#!/bin/bash

# Path to your image
image_path="data/intermediate/stitched_images/Goteborgs och Bohus.pdf_page_19_20.jpg"

# Your S3 bucket name
bucket="s3://electricity-tables"

# Command to copy the image to your S3 bucket
aws s3 cp "$image_path" "$bucket"
