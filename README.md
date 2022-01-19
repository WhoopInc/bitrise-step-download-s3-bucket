# bitrise-step-download-s3-bucket
Securely downloads the contents of an s3 bucket

---

## 🔴 This is a public repository 🔴

---
### Description
This is a Bitrise step to download a secure s3 object
xww
---
### Usage
- Add a step call within the desired workflow of your `bitrise.yml` to download an object as such:
```yaml
- git::https://github.com/WhoopInc/bitrise-step-download-s3-bucket.git@main:
     title: Download s3 bucket
     inputs:
        - client_id: $AWS_ACCESS_KEY
        - secret: $AWS_SECRET
        - bucket: "bucket"
        - region: "us-west-2"
        - object: "bucketfolder/object123.zip"
        - filename: "object.zip"
```