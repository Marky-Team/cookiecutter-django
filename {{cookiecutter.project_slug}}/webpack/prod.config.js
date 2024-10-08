const { merge } = require('webpack-merge');
const commonConfig = require('./common.config');

// This variable should mirror the one from config/settings/combined.py
{%- if cookiecutter.use_whitenoise == 'n' %}
const s3BucketName = process.env.DJANGO_AWS_STORAGE_BUCKET_NAME;
const awsS3Domain = process.env.DJANGO_AWS_S3_CUSTOM_DOMAIN
  ? process.env.DJANGO_AWS_S3_CUSTOM_DOMAIN
  : `${s3BucketName}.s3.amazonaws.com`;
const staticUrl = `https://${awsS3Domain}/static/`;
{%- else %}
const staticUrl = '/static/';
{%- endif %}

module.exports = merge(commonConfig, {
  mode: 'production',
  devtool: 'source-map',
  bail: true,
  output: {
    publicPath: `${staticUrl}webpack_bundles/`,
  },
});
