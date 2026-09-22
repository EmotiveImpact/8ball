"""Versioned starter catalogue. Examples are hypotheses, not professional advice.
No playbook is silently selected from free-text intake.
"""
from datetime import timedelta
from .contracts import *
from ..models import Evidence, Observation, utcnow

PLAYBOOK_VERSION='0.2.0'
PROVENANCE=Provenance(origin='playbook',note='8BALL starter catalogue 0.2.0. Illustrative estimates; specialist review required.')


def c(id,title,confirmation=None,**kwargs):
    return Condition(id=id,title=title,confirmation=confirmation or 'Review direct evidence of: '+title,
                     provenance=PROVENANCE,**kwargs)


def a(id,title,owner,requires,effects,minutes,cost=0,**kwargs):
    req=all_of(*requires) if isinstance(requires,list) else requires
    return Action(id=id,title=title,owner=owner,purpose=title,requires=req,
                  effects=[Effect(condition_id=e) if isinstance(e,str) else e for e in effects],
                  minutes=minutes,cost=cost,provenance=PROVENANCE,**kwargs)


def retention(now=None):
    now=now or utcnow()
    actors=[Actor(id='company',name='Aster Systems',kind='organisation',role='Service provider',provenance=PROVENANCE),
            Actor(id='customer',name='Northstar',kind='organisation',role='Customer considering continuation',provenance=PROVENANCE),
            Actor(id='coo',name='Customer COO',role='Reported escalation contact',authority='Continuation authority must be confirmed',provenance=PROVENANCE),
            Actor(id='engineering',name='Engineering',kind='team',role='Incident investigation and remediation',provenance=PROVENANCE),
            Actor(id='counsel',name='Legal adviser',kind='team',role='Review communications and constraints',provenance=PROVENANCE)]
    conditions=[c('records','Incident records preserved'),c('root','Root cause verified',actor_id='engineering'),
                c('contained','Immediate failure contained'),
                c('report','Incident report approved','Technical and case leads approve the report',due_at=now+timedelta(hours=12),criticality='critical'),
                c('language','External language approved','Written professional review of the proposed wording'),
                c('authority','Negotiation limits authorised'),
                c('requirements','Customer requirements confirmed',kind='external_state',actor_id='coo'),
                c('standstill','Standstill accepted in writing',kind='external_state',actor_id='customer'),
                c('refused','Standstill refused',kind='external_state',actor_id='customer'),
                c('silent','No response by review time',kind='external_state'),
                c('retained','Continuation agreement accepted','Written acceptance by the authorised parties',kind='target',criticality='critical')]
    actions=[a('preserve','Preserve incident records','Case lead',[],['records'],30,100),
             a('investigate','Verify the root cause','Technical lead',['records'],['root'],150,800,actor_ids=['engineering']),
             a('contain','Contain the service failure','Technical lead',['records'],['contained'],60,300),
             a('report','Prepare the incident report','Technical lead',['root','contained'],['report'],90,500,resources=['review-room']),
             a('language','Review external wording','Legal adviser',['records'],['language'],45,300,actor_ids=['counsel']),
             a('authority','Agree negotiation limits','Company director',[],['authority'],30,100),
             a('listen','Confirm customer requirements','Account director',['records','language'],['requirements'],30,100,approval_required=True,contingent=True,wait_minutes=None,actor_ids=['coo']),
             a('pause','Request a standstill','Account director',['contained','authority','language'],['standstill'],20,100,
               approval_required=True,contingent=True,wait_minutes=120,actor_ids=['coo'],
               contingencies=[Contingency(label='Accepted',when=atom('standstill'),response='Review the staged recovery route',next_action_ids=['staged']),
                              Contingency(label='Refused',when=atom('refused'),response='Consider the mediated alternative',next_action_ids=['mediated']),
                              Contingency(label='No response',when=atom('silent'),response='Review the escalation decision',due_at=now+timedelta(hours=4))]),
             a('direct','Direct recovery agreement','Account director',['report','requirements','authority','language'],['retained'],45,800,
               approval_required=True,contingent=True,wait_minutes=None,actor_ids=['customer'],risk='medium',
               side_effects=['Commercial concessions may affect future negotiations']),
             a('staged','Staged recovery agreement','Account director',['report','standstill','authority','language'],['retained'],120,500,
               approval_required=True,contingent=True,wait_minutes=60,actor_ids=['customer'],
               guard=atom('refused',False)),
             a('mediated','Mediated recovery agreement','External mediator',all_of('report','language','authority',any_of('requirements','refused')),['retained'],180,2200,
               approval_required=True,contingent=True,wait_minutes=180,actor_ids=['customer','counsel'],reversibility='difficult',risk='medium',
               decision_id='escalation',decision_option='mediate')]
    graph=Graph(conditions=conditions,actions=actions,objectives=[Objective(id='retain',title='Retain the customer by agreement',success=atom('retained'),provenance=PROVENANCE),
                     Objective(id='stabilise',title='Contain ongoing disruption',mandatory=False,priority=2,success=atom('contained'),provenance=PROVENANCE)])
    return {'graph':graph,'actors':actors,'relationships':[
        Relationship(id='r1',from_actor='customer',to_actor='company',kind='customer_of',provenance=PROVENANCE),
        Relationship(id='r2',from_actor='coo',to_actor='customer',kind='reported_representative',provenance=PROVENANCE),
        Relationship(id='r3',from_actor='counsel',to_actor='company',kind='advises',provenance=PROVENANCE)],
        'resources':[Resource(id='review-room',name='Technical report reviewer')],
        'decisions':[Decision(id='escalation',question='Should we seek a mediated resolution?',owner='Case lead',needed_by=now+timedelta(hours=6),
            options=[Option(id='mediate',title='Seek professional mediation'),Option(id='hold',title='Continue direct engagement')],provenance=PROVENANCE)],
        'questions':[Question(id='q_authority',question='Who can authorise the customer’s continuation agreement?',why='A positive reply from the wrong representative is not an accepted agreement.',condition_ids=['retained','requirements'],owner='Account director',provenance=PROVENANCE)],
        'constraints':[Constraint(id='no_speculation',title='No speculative claims in external communications',kind='communication',hard=True,confirmed=True,
                     predicate=atom('language'),action_ids=['listen','pause','direct','staged','mediated'],provenance=PROVENANCE)]}


CATALOGUE={
 'retention':('Customer recovery','Commercial','Retain a customer following service disruption.','retained'),
 'recovery':('Service recovery','Operations','Restore a service and verify acceptance.','accepted'),
 'supplier':('Supplier failure','Operations','Restore a disrupted supply arrangement.','accepted'),
 'communications':('Executive communications','Communications','Prepare a verified and professionally reviewed response.','accepted'),
 'compromise':('Account compromise','Security','Contain authorised-account exposure and verify recovery.','accepted'),
 'travel':('Travel disruption','Assistance','Arrange an accepted, feasible alternative itinerary.','accepted'),
 'dispute':('Contract dispute triage','Professional triage','Preserve records and agree a professionally reviewed next step.','accepted'),
 'reputation':('Reputation incident triage','Communications','Verify the issue, protect affected people and agree a response.','accepted'),
}

SCENARIOS={
 'recovery':('Service impact documented','Existing service repaired','Approved fallback active','Service owner','Repair existing service','Activate approved fallback'),
 'supplier':('Supply shortfall documented','Existing supplier recovery agreed','Alternative supplier approved','Operations lead','Agree supplier recovery','Qualify an alternative supplier'),
 'communications':('Relevant facts documented','Reviewed direct response prepared','Reviewed stakeholder briefing prepared','Communications adviser','Prepare direct response','Prepare stakeholder briefing'),
 'compromise':('Authorised account scope documented','Access securely recovered','Containment and recovery support arranged','Security specialist','Recover authorised access','Engage authorised recovery support'),
 'travel':('Travel constraints documented','Original booking amended','Alternative itinerary approved','Travel adviser','Amend the original booking','Arrange an approved alternative'),
 'dispute':('Relevant records preserved','Professional triage completed','Mediation triage completed','Qualified adviser','Obtain professional triage','Explore agreed mediation'),
 'reputation':('Reported issue verified','Remediation response prepared','Affected-party response prepared','Case lead','Prepare a remediation response','Prepare an affected-party response'),
}


def get_playbook(id,now=None):
    if id not in CATALOGUE:raise ValueError('Unknown playbook')
    if id=='retention':return retention(now)
    scope,first,second,owner,act1,act2=SCENARIOS[id]
    graph=Graph(conditions=[c('scope',scope),c('primary',first),c('alternative',second),
                           c('authority','Appropriate authority and review obtained'),
                           c('accepted','Resolution accepted and verified','Direct evidence against the agreed acceptance criteria',kind='target')],
                actions=[a('scope','Establish the situation scope','Case lead',[],['scope'],30,100),
                         a('authority','Obtain authority and specialist review',owner,['scope'],['authority'],60,300),
                         a('primary',act1,owner,['scope','authority'],['primary'],120,700),
                         a('alternative',act2,owner,['scope','authority'],['alternative'],60,1300,approval_required=True,reversibility='difficult'),
                         a('accept','Verify and agree the resolution','Case lead',any_of('primary','alternative'),['accepted'],30,100,
                           contingent=True,approval_required=True,wait_minutes=None)],
                objectives=[Objective(id='resolution',title=CATALOGUE[id][2],success=atom('accepted'),provenance=PROVENANCE)])
    return {'graph':graph,'questions':[Question(id='acceptance',question='What would prove the situation is resolved?',why='Define acceptance before selecting a route.',condition_ids=['accepted'],provenance=PROVENANCE)]}


def list_playbooks():
    return [{'id':i,'name':v[0],'domain':v[1],'description':v[2],'version':PLAYBOOK_VERSION,
             'review_status':'starter_requires_specialist_review','author':'8BALL product team',
             'conditions':len(get_playbook(i)['graph'].conditions),'actions':len(get_playbook(i)['graph'].actions)} for i,v in CATALOGUE.items()]


def make_case(title,client,summary,desired_outcome,deadline,budget=10000,playbook=None,**kwargs):
    contents=get_playbook(playbook) if playbook else {}
    return Case(title=title,client=client,summary=summary,desired_outcome=desired_outcome,deadline=deadline,budget=budget,
                status='active' if playbook else 'intake',**contents,**kwargs)


def demo_case(now=None):
    now=now or utcnow()
    case=Case(title='Northstar account recovery',client='Aster Systems · fictional',summary='A major customer is considering termination after a service failure. The team needs a verified report, clear authority and an accepted recovery agreement.',
              desired_outcome='Retain the customer under an accepted recovery agreement',deadline=now+timedelta(hours=24),
              budget=7000,status='stabilising',priority='time_sensitive',next_update=now+timedelta(hours=2),**retention(now))
    entries=[('e_preserve','Preservation log','Fictional case lead','Incident records have been preserved. Negotiation limits were authorised by the company director.', ['records','authority']),
             ('e_tech','Engineering update','Fictional technical lead','The immediate failure is contained. The root cause has not yet been verified.', ['contained']),
             ('e_customer','Customer email','Fictional customer COO','We need the approved incident report by noon tomorrow. We have not refused a standstill, but have not accepted it either.', [])]
    for id,title,source,text,truths in entries:
        case.evidence.append(Evidence(id=id,title=title,source=source,text=text,status='reviewed'))
        for cid in truths:
            case.observations.append(Observation(condition_id=cid,evidence_id=id,value=True,rationale='Fictional demonstration attestation'))
    case.observations.append(Observation(condition_id='refused',evidence_id='e_customer',value=False,rationale='Fictional source explicitly says no refusal'))
    case.events=[Event(id='incident',title='Service disruption reported',occurred_at=now-timedelta(hours=3),time_label='Three hours before this demo opened',actor_ids=['engineering'],provenance=PROVENANCE),
                 Event(id='notice',title='Customer requests an incident report',occurred_at=now-timedelta(minutes=50),time_label='Fictional demo timeline',actor_ids=['coo'],provenance=PROVENANCE)]
    return Case.model_validate(case.model_dump())
