"""Export versioned JSON contracts without instantiating a database or model."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from endstate.api import PlanRequest,PlanResponse
from endstate.course import CourseAnchor,CourseAssessment
from endstate.operating import OutcomeBrief,OperatingPlan
from endstate.intelligence.operating import OperatingPlanningSpec,WrittenReview,RevisedPlan


def export(output:Path):
    output.mkdir(parents=True,exist_ok=True)
    records={}
    for name,contract in [('endstate.plan.v1.request',PlanRequest),('endstate.plan.v1.response',PlanResponse),('endstate.course.v1.anchor',CourseAnchor),('endstate.course.v1.assessment',CourseAssessment),
        ('endstate.operating.v1.brief',OutcomeBrief),('endstate.operating.v1.plan',OperatingPlan),
        ('endstate.operating.v1.spec',OperatingPlanningSpec),('endstate.operating.v1.review',WrittenReview),
        ('endstate.operating.v1.revision',RevisedPlan)]:
        raw=(json.dumps(contract.model_json_schema(),indent=2,ensure_ascii=False)+'\n').encode()
        path=output/(name+'.json');path.write_bytes(raw)
        records[path.name]=hashlib.sha256(raw).hexdigest()
    (output/'SHA256SUMS.json').write_text(json.dumps(records,indent=2)+'\n')
    return records


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/'artifacts/endstate-schemas')
    print(json.dumps(export(parser.parse_args().output),indent=2))
