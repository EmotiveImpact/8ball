"""Real CPU inference experiment on a frozen fictional dataset.
Requires separately installed GLiClass and an explicit setup-time model download.
Never reads user cases, tokens or the application database. Not a production gate.
"""
from pathlib import Path
import hashlib,json,os,platform,resource,statistics,subprocess,sys,time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
OUT=Path(os.getenv('EIGHTBALL_EVAL_OUTPUT',str(ROOT/'artifacts/models')))
OUT.mkdir(parents=True,exist_ok=True)


def main():
    from huggingface_hub import HfApi,snapshot_download
    import torch
    from eightball.providers import G_MODEL,LABELS,gliclass_classify,_gliclass_pipeline
    torch.set_num_threads(2)
    raw=(ROOT/'evals/classification-cases.json').read_bytes();cases=json.loads(raw)
    revision=HfApi().model_info(G_MODEL).sha
    # Download only known model/tokeniser data, never arbitrary model Python code.
    snapshot_download(G_MODEL,revision=revision,allow_patterns=['*.json','*.safetensors','*.txt','*.model'])
    os.environ['EIGHTBALL_GLICLASS_REVISION']=revision
    started=time.perf_counter();pipe=_gliclass_pipeline();load=time.perf_counter()-started
    # Exercise the actual public application adapter, including abstention/validation.
    predictions=[]
    for item in cases:
        start=time.perf_counter();result=gliclass_classify(item['text'])
        predicted=max(result['scores'],key=result['scores'].get)
        predictions.append({**item,'raw_prediction':predicted,'adapter_label':result['label'],
                            'abstained':result['abstained'],'scores':result['scores'],
                            'latency_ms':round((time.perf_counter()-start)*1000,2)})
    per_class={}
    for label in LABELS:
        tp=sum(x['raw_prediction']==label and x['label']==label for x in predictions)
        selected=sum(x['raw_prediction']==label for x in predictions)
        actual=sum(x['label']==label for x in predictions)
        per_class[label]={'support':actual,'true_positive':tp,'precision':tp/selected if selected else None,'recall':tp/actual if actual else None}
    covered=[p for p in predictions if not p['abstained']]
    report={'status':'completed','actual_model_inference':True,'model':G_MODEL,'model_revision':revision,
            'dataset_sha256':hashlib.sha256(raw).hexdigest(),'dataset_size':len(cases),
            'dataset_description':'Fictional author-labelled challenge set, fixed before this run; not independent expert validation.',
            'application_adapter':'eightball.providers.gliclass_classify','device':'CPU','threads':2,
            'load_seconds':round(load,3),'raw_top1_accuracy':sum(p['raw_prediction']==p['label'] for p in predictions)/len(predictions),
            'coverage_after_existing_abstention':len(covered)/len(predictions),
            'covered_accuracy':sum(p['raw_prediction']==p['label'] for p in covered)/len(covered) if covered else None,
            'latency_median_ms':statistics.median(p['latency_ms'] for p in predictions),
            'process_peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
            'python':platform.python_version(),'per_class':per_class,'predictions':predictions,
            'production_approved':False,'all_outputs_require_human_review':True,
            'limitations':['Small synthetic set; author labels may be contestable.','No calibration, case-resolution or graph-planning accuracy claim.','Pipeline scores are not probabilities of resolving a case.','No threshold tuning was performed on this dataset.']}
    (OUT/'gliclass-live-report.json').write_text(json.dumps(report,indent=2))
    (OUT/'model-environment.txt').write_text(subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True))
    print(json.dumps({k:v for k,v in report.items() if k!='predictions'},indent=2))


if __name__=='__main__':
    try:main()
    except Exception as e:
        (OUT/'model-error.json').write_text(json.dumps({'status':'failed','exception_type':type(e).__name__,'message':str(e)[:2000]},indent=2))
        raise
