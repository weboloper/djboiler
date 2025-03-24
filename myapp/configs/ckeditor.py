CKEDITOR_5_ALLOW_ALL_FILE_TYPES = True
CKEDITOR_5_UPLOAD_FILE_TYPES = ['jpeg', 'pdf', 'png'] # optional
CKEDITOR_5_CONFIGS = {
  'default': {
      'toolbar': ['heading', '|', 'essentials', 'code', 'imageStle', 'image', 'bold', 'italic', 'link',
                  'ImageCaption',
                  'indent',
                  'indentBlock',
	'imageInline',
	'imageInsert',
	'iImageInsertViaUrl',
	'imageResize',
	'imageStyle',
	'iImageTextAlternative',
	'imageToolbar',
	
                  'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', 'fileUpload', 'alignment', 'imageToolbar', 'mediaEmbed','imageInsert' ], # include fileUpload here
      'language': 'tr',
    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
 
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        }
    }
}
CK_EDITOR_5_UPLOAD_FILE_VIEW_NAME = "custom_upload_file"