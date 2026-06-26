---
layout: default
title: N3-Infrastructure-CICD HTTP2
---

Why does HTTP/2 break file downloads?
HTTP/2 multiplexes streams and handles headers differently.
Some proxies/load balancers (including AWS ALB) have bugs or limitations with binary streaming, especially when using Content-Disposition: attachment for downloads.
Nginx and PHP/Laravel may send responses that are valid for HTTP/1.1, but the ALB can mishandle them under HTTP/2, causing corrupted downloads, incomplete files, or protocol errors.
Browsers may also expect certain header behaviors that get lost in translation through ALB+HTTP/2.
How to make it work with HTTP/2?
1. Use S3 Signed URLs for Downloads
Instead of proxying the file through Laravel/Nginx, generate a signed S3 URL and redirect the user to it. S3 handles binary downloads perfectly with HTTP/2.

2. Serve Files Directly from S3 (Frontend)
If possible, let your frontend request the file directly from S3 using a signed URL.

3. Tune Nginx and PHP
Make sure output_buffering is off in PHP.
Set proxy_buffering off; in Nginx for download endpoints.
Disable gzip for binary files.
4. Chunked Responses
If you must stream files, use chunked responses and ensure your Nginx and PHP are configured for large files and streaming.

5. Check ALB and Nginx Updates
Sometimes, newer versions of ALB and Nginx fix these issues. Make sure you are using the latest stable releases.

6. Fallback: Use HTTP/1.1 for Downloads
If you can't change your architecture, keep HTTP/2 enabled for most traffic, but route download endpoints through a separate listener or path that uses HTTP/1.1.

Summary
Root cause: AWS ALB + HTTP/2 mishandles binary file downloads proxied from PHP/Nginx.
Best solution: Use S3 signed URLs for downloads.
Alternative: Tune Nginx/PHP for streaming, or use HTTP/1.1 for download endpoints.
