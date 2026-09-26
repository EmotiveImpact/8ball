from datetime import datetime, timezone
import pytest
from pydantic import ValidationError
from endstate.time_review import TimeInterpretation, interpret_time


def spec(**kw):
    return TimeInterpretation(**{'calendar_date':'2026-09-24','wall_time':'12:00','time_zone':'Europe/London',
                                 'zone_reason':'Source explicitly says London time',**kw})


def test_london_summer_time_converts_to_utc():
    result=interpret_time(spec())
    assert result['status']=='resolved'
    assert result['selected']['utc']=='2026-09-24T11:00:00+00:00'
    assert result['selected']['offset_seconds']==3600


def test_repeated_time_requires_deliberate_choice():
    result=interpret_time(spec(calendar_date='2026-10-25',wall_time='01:30'))
    assert result['status']=='ambiguous' and result['selected'] is None
    assert [o['utc'] for o in result['options']]==['2026-10-25T00:30:00+00:00','2026-10-25T01:30:00+00:00']
    for fold in [0,1]:
        out=interpret_time(spec(calendar_date='2026-10-25',wall_time='01:30',fold=fold))
        assert out['selected']['fold']==fold


def test_missing_time_not_silently_shifted():
    result=interpret_time(spec(calendar_date='2026-03-29',wall_time='01:30'))
    assert result['status']=='nonexistent' and not result['options']
    assert result['selected'] is None


def test_relative_date_has_an_explicit_anchor_not_machine_now():
    s=spec(basis='relative_days',calendar_date=None,anchor_date='2026-09-23',day_offset=1,
           anchor_reason='Source written on 23 September, not its import date')
    out=interpret_time(s)
    assert out['calendar_date']=='2026-09-24'
    assert out['basis']['anchor_reason'].startswith('Source written')


@pytest.mark.parametrize('kw',[
 {'basis':'relative_days','calendar_date':None,'day_offset':1},
 {'basis':'relative_days','calendar_date':None,'anchor_date':'2026-09-24','day_offset':1},
 {'basis':'absolute','anchor_date':'2026-09-24'},
 {'calendar_date':'24/09/2026'}, {'calendar_date':'03/04/2026'}, {'calendar_date':'2026-02-30'},
 {'wall_time':'24:00'}, {'wall_time':'12:61'}, {'wall_time':'9:30'}, {'wall_time':'noon'},
 {'fold':True}, {'fold':2}, {'zone_reason':'   '}, {'time_zone':' Europe/London'},
])
def test_ambiguous_or_invalid_inputs_are_not_guessed(kw):
    with pytest.raises((ValidationError,ValueError)):spec(**kw)


@pytest.mark.parametrize('zone',['BST','EST','CST','Unknown/Nowhere','../Etc/UTC','posix/Europe/London','right/UTC'])
def test_timezone_abbreviations_and_invalid_paths_rejected(zone):
    with pytest.raises(ValueError):interpret_time(spec(time_zone=zone))


def test_fold_cannot_be_silently_ignored_on_normal_time():
    with pytest.raises(ValueError,match='not ambiguous'):interpret_time(spec(fold=1))


@pytest.mark.parametrize('zone,expected',[
 ('UTC','2026-09-24T12:00:00+00:00'),
 ('Asia/Kolkata','2026-09-24T06:30:00+00:00'),
 ('Asia/Kathmandu','2026-09-24T06:15:00+00:00'),
 ('America/New_York','2026-09-24T16:00:00+00:00'),
])
def test_non_london_and_fractional_offsets(zone,expected):
    assert interpret_time(spec(time_zone=zone))['selected']['utc']==expected


def test_calendar_arithmetic_can_cross_year():
    out=interpret_time(spec(basis='relative_days',calendar_date=None,anchor_date='2026-12-31',day_offset=1,anchor_reason='Document explicitly dated on New Year’s Eve'))
    assert out['calendar_date']=='2027-01-01'


def test_out_of_range_relative_date_is_rejected():
    with pytest.raises(ValueError):interpret_time(spec(basis='relative_days',calendar_date=None,anchor_date='9999-12-31',day_offset=1,anchor_reason='Source date stated'))


def test_time_review_imports_no_application_or_network_packages(tmp_path):
    import pathlib,shutil,subprocess,sys
    root=pathlib.Path(__file__).resolve().parents[1]
    shutil.copytree(root/'endstate',tmp_path/'endstate',ignore=shutil.ignore_patterns('__pycache__'))
    script='''
import sys,importlib.abc
sys.path.insert(0,sys.argv[1])
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,name,*a,**kw):
  if name.split('.')[0] in ('eightball','httpx','fastapi','sqlite3'):
   raise AssertionError('Unexpected runtime import: '+name)
sys.meta_path.insert(0,Deny())
from endstate.time_review import TimeInterpretation,interpret_time
r=interpret_time(TimeInterpretation(calendar_date='2026-09-24',wall_time='12:00',time_zone='UTC',zone_reason='Explicit UTC source'))
assert r['selected']['utc']=='2026-09-24T12:00:00+00:00'
'''
    subprocess.run([sys.executable,'-I','-c',script,str(tmp_path)],check=True,capture_output=True,text=True)


def test_mutated_model_instance_is_revalidated_at_calculation_boundary():
    broken=spec().model_copy(update={'fold':True})
    with pytest.raises(ValidationError):interpret_time(broken)
