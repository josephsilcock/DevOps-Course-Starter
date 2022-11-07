# Docker

We have logging set up. You can change the log level by setting the environment variable `LOG_LEVEL` to one of:
- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

## Loggly

We also have logging to [loggly](https://www.loggly.com/) set up. To use this:
- Create an account with Loggly
- Once you've created your account, log in and find the icon for "Logs" in the lefthand menu. Under this, select 
  "Source Setup". Then, on the tabs along the top of the page, select "Customer Tokens". Add a new customer token.
- Set this token as en environment variable called `LOGGLY_TOKEN`