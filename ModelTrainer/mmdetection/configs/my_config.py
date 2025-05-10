_base_ = [r'mmdetection\configs\faster_rcnn\faster-rcnn_r50_fpn_1x_coco.py'
]

dataset_type = 'CocoDataset'
data_root = r'C:/Projects/MastersThesis/ImageLocator/annotations/'
classes = ('bargraph', 'chart', 'damper', 'fan', 'line', 'mixer',
           'motor', 'nav', 'pump', 'status', 'tag', 'value', 'valve', 'pipe') 
num_classes = len(classes)

metainfo = {
    'classes': classes,
}

model = dict(
    roi_head=dict(
        bbox_head=dict(num_classes=num_classes)
    )
)

train_dataloader = dict(
    dataset=dict(
        data_root=data_root,
        ann_file='train.json',
        data_prefix=dict(img='images/train/'),
        metainfo=metainfo
    )
)

val_dataloader = dict(
    dataset=dict(
        data_root=data_root,
        ann_file='val.json',
        data_prefix=dict(img='images/val/'),
        metainfo=metainfo
    )
)

test_dataloader = val_dataloader

val_evaluator = dict(
    type='CocoMetric',
    ann_file=data_root + 'val.json',
    metric=['bbox'],
    format_only=False,
    backend_args=None
)


test_evaluator = val_evaluator

train_cfg = dict(
    type='EpochBasedTrainLoop',
    max_epochs=1,  
    val_interval=1)  
val_cfg = dict(type='ValLoop')  
test_cfg = dict(type='TestLoop') 


default_hooks = dict(
    logger=dict(type='LoggerHook', interval=10),  
    checkpoint=dict(interval=10),
    timer=dict(type='IterTimerHook')
)

log_processor = dict(
    type='LogProcessor',
    window_size=10,
    by_epoch=True
)

visualizer = dict(
    type='DetLocalVisualizer',
    vis_backends=[
        dict(type='LocalVisBackend'),
    ],
    name='visualizer'
)

resume_from = 'work_dirs/my_model/epoch_6.pth'