---
title: "Javascript Calendar"
date: 2014-01-05T00:00:00-00:00
last_modified_at: 2014-01-05T00:00:00-00:00
categories:
  - webdev
  - school project
permalink: /post-javascript-calendar/
classes: wide
excerpt: A simple calendar coded in JS, Jquery, php and mySQL
header:
  og_image: /images/js-calendar/1.jpg
  teaser: /images/js-calendar/1.jpg
---

<figure class="half">
    <img src="/images/js-calendar/0.jpg">
    <img src="/images/js-calendar/1.jpg">
</figure>

This is a simple calendar coded in JS, Jquery, php and mySQL.  It has a few special features, but it is built primarily around AJAX events

- Passwords are stored salted and encrypted.
- All AJAX requests that either contain sensitive information or modify something on the server are performed via POST, not GET
- Safe from XSS attacks; that is, all content is escaped on output
- Safe from SQL Injection attacks
- CSRF tokens are passed when editing or removing events
- Session cookie is HTTP-Only
- Page passes the W3C validator

You can see the src code here: [bitbucket.org/dcyoung/javascript-calendar/src](https://bitbucket.org/dcyoung/javascript-calendar/src)