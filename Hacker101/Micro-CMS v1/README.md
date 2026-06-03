# Micro-CMS v1 -- Writeup

This challenge simulates a minimal content management system (CMS) that
allows users to create and edit webpages using Markdown. Several flaws
in access control, input sanitization, and Markdown rendering lead to
multiple flags.

------------------------------------------------------------------------

## Flag 0 -- Access Control Misconfiguration

While exploring the application, I notice two existing pages with IDs
**1** and **2** (visible in the URL).\
After creating a new page, its assigned ID is **11**, suggesting that
additional pages might exist but are not directly linked.

By manually changing the page ID in the URL, most pages return **404**,
except for one that returns **403**, indicating the page exists but is
restricted.

Because the editing route follows the same ID pattern (`/page/{id}` →
`/page/edit/{id}`), accessing the **edit** version of the restricted
page bypasses the authorization check. This exposes its content,
revealing the flag in plaintext.

------------------------------------------------------------------------

## Flag 1 -- SQL Injection in Edit Route

While testing for SQL injection vulnerabilities, I discover that the
endpoint:

    /page/edit/{id}

is vulnerable to SQLi.\
A payload such as:

    /page/edit/11' --

breaks the query and confirms the injection point, allowing retrieval of
the flag associated with this vulnerability.

------------------------------------------------------------------------

## Flag 2 -- Stored XSS via Page Title

To obtain this flag, I exploit a stored XSS vulnerability in the page
title field. When the page is rendered, the title is injected directly
into the HTML without sanitization.

A simple payload like:

``` html
c<script>alert(1)</script>C
```

successfully triggers a JavaScript alert, which displays the flag.

------------------------------------------------------------------------

## Flag 3 -- Markdown Injection Leading to HTML Execution

For the final flag, modify the existing **"Markdown Test"** page. This
page includes a button rendered through Markdown.

By injecting an `onclick` attribute into the button element, we can
execute JavaScript when it is pressed. The flag becomes
visible in the resulting HTML code in and attribute of this button.

------------------------------------------------------------------------

## Summary

Micro-CMS v1 demonstrates a combination of common web vulnerabilities:

-   Insecure Direct Object Reference (IDOR)
-   SQL Injection
-   Stored XSS
-   Unsafe Markdown-to-HTML handling

Exploiting these flaws reveals all four flags and highlights the
importance of proper input validation, authorization checks, and secure
rendering pipelines.
