from flask import render_template, request, redirect, url_for, \
    current_app
import os
import json
import boto3
from app.upload import bp


@bp.route('/sign_s3/')
def sign_s3():
    S3_BUCKET = current_app.config['S3_BUCKET']

    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')

    session = boto3.Session(
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
        region_name=current_app.config['REGION_NAME']
    )

    s3 = session.client('s3')

    presigned_post = s3.generate_presigned_post(
        Bucket=S3_BUCKET,
        Key=file_name,
        Fields={"acl": "public-read", "Content-Type": file_type},
        Conditions=[
            {"acl": "public-read"},
            {"Content-Type": file_type}
        ],
        ExpiresIn=3600
    )

    return json.dumps({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
    })
