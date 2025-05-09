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
    type='CocoMetric',  # COCO metric
    ann_file=data_root + 'val.json',  # Path to the validation annotations
    metric=['bbox'],  # You can add 'segm' for instance segmentation if applicable
    format_only=False,
    backend_args=None  # If needed, add backend args for specific file systems (optional)
)

# The test evaluator is typically the same as the validation evaluator
test_evaluator = val_evaluator

train_cfg = dict(
    type='EpochBasedTrainLoop',  # The training loop type. Refer to https://github.com/open-mmlab/mmengine/blob/main/mmengine/runner/loops.py
    max_epochs=1,  # Maximum training epochs
    val_interval=1)  # Validation intervals. Run validation every epoch.
val_cfg = dict(type='ValLoop')  # The validation loop type
test_cfg = dict(type='TestLoop')  # The testing loop type

# Add the evaluation section to training hooks
default_hooks = dict(
    logger=dict(type='LoggerHook', interval=10),  # log every iteration
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