import sys
import datetime

from idds.common.utils import json_dumps                 # noqa F401
from idds.common.constants import ContentStatus, ContentType, ContentRelationType, ContentLocking          # noqa F401
from idds.core.requests import get_requests              # noqa F401
from idds.core.messages import retrieve_messages         # noqa F401
from idds.core.transforms import get_transforms          # noqa F401
from idds.core.workprogress import get_workprogresses    # noqa F401
from idds.core.processings import get_processings        # noqa F401
from idds.core import transforms as core_transforms      # noqa F401
from idds.orm.contents import get_input_contents
from idds.core.transforms import release_inputs_by_collection, release_inputs_by_collection_old     # noqa F401


def release_inputs_test():
    to_release_inputs = {3498: [{'map_id': 1, 'status': ContentStatus.Available, 'retries': 0, 'scope': 'pseudo_dataset',
                                 'substatus': ContentStatus.Available, 'path': None,
                                 'name': 'u_jchiang_dark_12781_panda_20210712T222923Z.qgraph+3_isr_3020111900038_94+qgraphNodeId:3+qgraphId:1626129062.5744567-119392',
                                 'content_id': 2248918, 'min_id': 0, 'bytes': 1, 'coll_id': 3498, 'max_id': 1, 'md5': None,
                                 'request_id': 93, 'content_type': ContentType.File, 'adler32': '12345678',
                                 'workload_id': 1626129080, 'content_relation_type': ContentRelationType.Output,
                                 'processing_id': None, 'content_metadata': {'events': 1, 'panda_id': 1411522}, 'transform_id': 1749, 'storage_id': None},
                                {'map_id': 2, 'status': ContentStatus.Available, 'retries': 0, 'scope': 'pseudo_dataset',
                                 'substatus': ContentStatus.Available, 'path': None,
                                 'name': 'u_jchiang_dark_12781_panda_20210712T222923Z.qgraph+2_isr_3020111900032_94+qgraphNodeId:2+qgraphId:1626129062.5744567-119392',
                                 'content_id': 2248919, 'min_id': 0, 'bytes': 1, 'coll_id': 3498, 'max_id': 1, 'md5': None,
                                 'request_id': 93, 'content_type': ContentType.File, 'adler32': '12345678',
                                 'workload_id': 1626129080, 'content_relation_type': ContentRelationType.Output,
                                 'processing_id': None, 'content_metadata': {'events': 1, 'panda_id': 1411523}, 'transform_id': 1749, 'storage_id': None},
                                {'map_id': 3, 'status': ContentStatus.Available, 'retries': 0, 'scope': 'pseudo_dataset',
                                 'substatus': ContentStatus.Available, 'path': None,
                                 'name': 'u_jchiang_dark_12781_panda_20210712T222923Z.qgraph+4_isr_3020111900040_94+qgraphNodeId:4+qgraphId:1626129062.5744567-119392',
                                 'content_id': 2248920, 'min_id': 0, 'bytes': 1, 'coll_id': 3498, 'max_id': 1, 'md5': None,
                                 'request_id': 93, 'content_type': ContentType.File, 'adler32': '12345678',
                                 'workload_id': 1626129080, 'content_relation_type': ContentRelationType.Output,
                                 'processing_id': None, 'content_metadata': {'events': 1, 'panda_id': 1411524}, 'transform_id': 1749, 'storage_id': None},
                                {'map_id': 4, 'status': ContentStatus.Available, 'retries': 0, 'scope': 'pseudo_dataset',
                                 'substatus': ContentStatus.Available, 'path': None,
                                 'name': 'u_jchiang_dark_12781_panda_20210712T222923Z.qgraph+1_isr_3020111900036_94+qgraphNodeId:1+qgraphId:1626129062.5744567-119392',
                                 'content_id': 2248921, 'min_id': 0, 'bytes': 1, 'coll_id': 3498, 'max_id': 1, 'md5': None,
                                 'request_id': 93, 'content_type': ContentType.File, 'adler32': '12345678',
                                 'workload_id': 1626129080, 'content_relation_type': ContentRelationType.Output,
                                 'processing_id': None, 'content_metadata': {'events': 1, 'panda_id': 1411525}, 'transform_id': 1749, 'storage_id': None},
                                {'map_id': 5, 'status': ContentStatus.Available, 'retries': 0, 'scope': 'pseudo_dataset',
                                 'substatus': ContentStatus.Available, 'path': None,
                                 'name': 'u_jchiang_dark_12781_panda_20210712T222923Z.qgraph+0_isr_3020111900034_94+qgraphNodeId:0+qgraphId:1626129062.5744567-119392',
                                 'content_id': 2248922, 'min_id': 0, 'bytes': 1, 'coll_id': 3498, 'max_id': 1, 'md5': None,
                                 'request_id': 93, 'content_type': ContentType.File, 'adler32': '12345678',
                                 'workload_id': 1626129080, 'content_relation_type': ContentRelationType.Output,
                                 'processing_id': None, 'content_metadata': {'events': 1, 'panda_id': 1411526}, 'transform_id': 1749, 'storage_id': None}
                                ]}

    to_release_inputs = {4042: [{'map_id': 1, 'status': ContentStatus.Available, 'retries': 0, 'scope': 'pseudo_dataset', 'substatus': ContentStatus.Available, 'path': None, 'name': 'u_huanlin_panda_test_ci_imsim_w26_20210714T214732Z.qgraph+13_isr_257768_161+1626299263.3909254-24148+13', 'locking': ContentLocking.Idle, 'created_at': datetime.datetime(2021, 7, 14, 21, 48, 10), 'content_id': 2254913, 'min_id': 0, 'bytes': 1, 'updated_at': datetime.datetime(2021, 7, 14, 22, 8, 30), 'coll_id': 4042, 'max_id': 1, 'md5': None, 'accessed_at': datetime.datetime(2021, 7, 14, 22, 8, 30), 'request_id': 107, 'content_type': ContentType.File, 'adler32': '12345678', 'expired_at': datetime.datetime(2021, 8, 13, 21, 48, 10), 'workload_id': 1626299273, 'content_relation_type': ContentRelationType.Output, 'processing_id': None, 'content_metadata': {'events': 1, 'panda_id': 1412272}, 'transform_id': 2021, 'storage_id': None},   # noqa E501
                               {'map_id': 2, 'status': ContentStatus.Available, 'retries': 0, 'scope': 'pseudo_dataset', 'substatus': ContentStatus.Available, 'path': None, 'name': 'u_huanlin_panda_test_ci_imsim_w26_20210714T214732Z.qgraph+2_isr_212071_54+1626299263.3909254-24148+2', 'locking': ContentLocking.Idle, 'created_at': datetime.datetime(2021, 7, 14, 21, 48, 10), 'content_id': 2254914, 'min_id': 0, 'bytes': 1, 'updated_at': datetime.datetime(2021, 7, 14, 22, 8, 30), 'coll_id': 4042, 'max_id': 1, 'md5': None, 'accessed_at': datetime.datetime(2021, 7, 14, 22, 8, 30), 'request_id': 107, 'content_type': ContentType.File, 'adler32': '12345678', 'expired_at': datetime.datetime(2021, 8, 13, 21, 48, 10), 'workload_id': 1626299273, 'content_relation_type': ContentRelationType.Output, 'processing_id': None, 'content_metadata': {'events': 1, 'panda_id': 1412273}, 'transform_id': 2021, 'storage_id': None},   # noqa E501
                              {'map_id': 3, 'status': ContentStatus.Available, 'retries': 0, 'scope': 'pseudo_dataset', 'substatus': ContentStatus.Available, 'path': None, 'name': 'u_huanlin_panda_test_ci_imsim_w26_20210714T214732Z.qgraph+10_isr_456716_99+1626299263.3909254-24148+10', 'locking': ContentLocking.Idle, 'created_at': datetime.datetime(2021, 7, 14, 21, 48, 10), 'content_id': 2254915, 'min_id': 0, 'bytes': 1, 'updated_at': datetime.datetime(2021, 7, 14, 22, 8, 30), 'coll_id': 4042, 'max_id': 1, 'md5': None, 'accessed_at': datetime.datetime(2021, 7, 14, 22, 8, 30), 'request_id': 107, 'content_type': ContentType.File, 'adler32': '12345678', 'expired_at': datetime.datetime(2021, 8, 13, 21, 48, 10), 'workload_id': 1626299273, 'content_relation_type': ContentRelationType.Output, 'processing_id': None, 'content_metadata': {'events': 1, 'panda_id': 1412274}, 'transform_id': 2021, 'storage_id': None},   # noqa E501
                              {'map_id': 4, 'status': ContentStatus.Available, 'retries': 0, 'scope': 'pseudo_dataset', 'substatus': ContentStatus.Available, 'path': None, 'name': 'u_huanlin_panda_test_ci_imsim_w26_20210714T214732Z.qgraph+34_isr_407919_130+1626299263.3909254-24148+34', 'locking': ContentLocking.Idle, 'created_at': datetime.datetime(2021, 7, 14, 21, 48, 10), 'content_id': 2254916, 'min_id': 0, 'bytes': 1, 'updated_at': datetime.datetime(2021, 7, 14, 22, 8, 30), 'coll_id': 4042, 'max_id': 1, 'md5': None, 'accessed_at': datetime.datetime(2021, 7, 14, 22, 8, 30), 'request_id': 107, 'content_type': ContentType.File, 'adler32': '12345678', 'expired_at': datetime.datetime(2021, 8, 13, 21, 48, 10), 'workload_id': 1626299273, 'content_relation_type': ContentRelationType.Output, 'processing_id': None, 'content_metadata': {'events': 1, 'panda_id': 1412275}, 'transform_id': 2021, 'storage_id': None},   # noqa E501
                              {'map_id': 5, 'status': ContentStatus.Available, 'retries': 0, 'scope': 'pseudo_dataset', 'substatus': ContentStatus.Available, 'path': None, 'name': 'u_huanlin_panda_test_ci_imsim_w26_20210714T214732Z.qgraph+23_isr_254379_48+1626299263.3909254-24148+23', 'locking': ContentLocking.Idle, 'created_at': datetime.datetime(2021, 7, 14, 21, 48, 10), 'content_id': 2254917, 'min_id': 0, 'bytes': 1, 'updated_at': datetime.datetime(2021, 7, 14, 22, 8, 30), 'coll_id': 4042, 'max_id': 1, 'md5': None, 'accessed_at': datetime.datetime(2021, 7, 14, 22, 8, 30), 'request_id': 107, 'content_type': ContentType.File, 'adler32': '12345678', 'expired_at': datetime.datetime(2021, 8, 13, 21, 48, 10), 'workload_id': 1626299273, 'content_relation_type': ContentRelationType.Output, 'processing_id': None, 'content_metadata': {'events': 1, 'panda_id': 1412276}, 'transform_id': 2021, 'storage_id': None},   # noqa E501
                             {'map_id': 6, 'status': ContentStatus.Available, 'retries': 0, 'scope': 'pseudo_dataset', 'substatus': ContentStatus.Available, 'path': None, 'name': 'u_huanlin_panda_test_ci_imsim_w26_20210714T214732Z.qgraph+11_isr_37657_141+1626299263.3909254-24148+11', 'locking': ContentLocking.Idle, 'created_at': datetime.datetime(2021, 7, 14, 21, 48, 10), 'content_id': 2254918, 'min_id': 0, 'bytes': 1, 'updated_at': datetime.datetime(2021, 7, 14, 22, 8, 30), 'coll_id': 4042, 'max_id': 1, 'md5': None, 'accessed_at': datetime.datetime(2021, 7, 14, 22, 8, 30), 'request_id': 107, 'content_type': ContentType.File, 'adler32': '12345678', 'expired_at': datetime.datetime(2021, 8, 13, 21, 48, 10), 'workload_id': 1626299273, 'content_relation_type': ContentRelationType.Output, 'processing_id': None, 'content_metadata': {'events': 1, 'panda_id': 1412277}, 'transform_id': 2021, 'storage_id': None},   # noqa E501
                            {'map_id': 7, 'status': ContentStatus.Available, 'retries': 0, 'scope': 'pseudo_dataset', 'substatus': ContentStatus.Available, 'path': None, 'name': 'u_huanlin_panda_test_ci_imsim_w26_20210714T214732Z.qgraph+31_isr_226983_36+1626299263.3909254-24148+31', 'locking': ContentLocking.Idle, 'created_at': datetime.datetime(2021, 7, 14, 21, 48, 10), 'content_id': 2254919, 'min_id': 0, 'bytes': 1, 'updated_at': datetime.datetime(2021, 7, 14, 22, 8, 30), 'coll_id': 4042, 'max_id': 1, 'md5': None, 'accessed_at': datetime.datetime(2021, 7, 14, 22, 8, 30), 'request_id': 107, 'content_type': ContentType.File, 'adler32': '12345678', 'expired_at': datetime.datetime(2021, 8, 13, 21, 48, 10), 'workload_id': 1626299273, 'content_relation_type': ContentRelationType.Output, 'processing_id': None, 'content_metadata': {'events': 1, 'panda_id': 1412278}, 'transform_id': 2021, 'storage_id': None}]}   # noqa E501

    for coll_id in to_release_inputs:
        contents = get_input_contents(request_id=to_release_inputs[coll_id][0]['request_id'],
                                      coll_id=coll_id,
                                      name=None)
        print(len(contents))
        in_dep_contents = []
        for content in contents:
            if (content['content_relation_type'] == ContentRelationType.InputDependency):
                in_dep_contents.append(content)
    print(len(in_dep_contents))

    update_contents = release_inputs_by_collection(to_release_inputs)
    print(update_contents)

    update_contents = release_inputs_by_collection(to_release_inputs, final=True)
    print(update_contents)


# release_inputs_test()


def show_works(req):
    workflow = req['processing_metadata']['workflow']
    print(workflow.independent_works)
    print(len(workflow.independent_works))
    print(workflow.works_template.keys())
    print(len(workflow.works_template.keys()))
    print(workflow.work_sequence.keys())
    print(len(workflow.work_sequence.keys()))
    print(workflow.works.keys())
    print(len(workflow.works.keys()))

    work_ids = []
    for i_id in workflow.works:
        work = workflow.works[i_id]
        print(i_id)
        print(work.work_name)
        print(work.task_name)
        print(work.work_id)
        work_ids.append(work.work_id)
    print(work_ids)


# reqs = get_requests(request_id=599, with_detail=True, with_metadata=True)
reqs = get_requests(request_id=599, with_request=True, with_detail=False, with_metadata=True)
for req in reqs:
    # print(req['request_id'])
    # print(rets)
    print(json_dumps(req, sort_keys=True, indent=4))
    # show_works(req)
    pass
    workflow = req['request_metadata']['workflow']
    if hasattr(workflow, 'get_relation_map'):
        # print(json_dumps(workflow.get_relation_map(), sort_keys=True, indent=4))
        pass

sys.exit(0)

"""
# reqs = get_requests()
# print(len(reqs))
for req in reqs:
    if req['request_id'] == 113:
        # print(req)
        # print(req['request_metadata']['workflow'].to_dict())
        # print(json_dumps(req, sort_keys=True, indent=4))
        pass

sys.exit(0)

"""

tfs = get_transforms(request_id=241)
for tf in tfs:
    # print(tf)
    # print(tf['transform_metadata']['work'].to_dict())
    print(json_dumps(tf, sort_keys=True, indent=4))
    pass

sys.exit(0)

"""
msgs = retrieve_messages(workload_id=25972557)
number_contents = 0
for msg in msgs:
    # if msg['msg_id'] in [323720]:
    # if True:
    # if msg['request_id'] in [208]:
    print(json_dumps(msg['msg_content'], sort_keys=True, indent=4))
    if msg['msg_content']['msg_type'] == 'file_stagein' and msg['msg_content']['relation_type'] == 'output':
        # number_contents += len(msg['msg_content']['files'])
        for i_file in msg['msg_content']['files']:
            if i_file['status'] == 'Available':
                number_contents += 1
    pass
print(number_contents)

sys.exit(0)
"""

prs = get_processings(request_id=219)
i = 0
for pr in prs:
    # if pr['request_id'] == 91:
    print("processing_number: %s" % i)
    i += 1
    print(json_dumps(pr, sort_keys=True, indent=4))
    pass

sys.exit(0)

to_release_inputs = [{'request_id': 248,
                      'coll_id': 3425,
                      'name': 'shared_pipecheck_20210407T110240Z.qgraph',
                      'status': ContentStatus.Available,
                      'substatus': ContentStatus.Available}]
# updated_contents = core_transforms.release_inputs(to_release_inputs)
# print(updated_contents)
