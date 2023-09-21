# python-cert-authority
<h3>Python Certification Authority</h3>
With the brief assistance of ChatGPT (with the cryptography library) - here are two python scripts that'll help you make your own certification authority.

I used Python 3.11.3 to make this - please use 3.11+ for the best compatibility.

1. Download both .py files
2. Open CMD or Powershell (Windows) - or your chosen terminal for Linux.
3. Execute <b>generate_ca.py</b> with your chosen arguments.
4. Execute <b>generate_cert_with_authority.py</b> with your chosen arguments.
5. Once you have both certificates - since they're self signed, your web browser won't like it - use the <b>import_cert_windows.py</b> to help. (For Linux: use Google as some distros do it different than others).

<hr>

<u>Generating the CA</u>
This is the syntax for generating your CA cert.

<code>python3 generate_ca.py <common_name> <org_name> <town_name> <state_name> <country_initials></code>

Let's say I want to generate a certificate for GitHub, the command would be:
<br><br>
<code>python3 generate_ca.py 'GitHub' 'GitHub' 'San Francisco' 'California' 'US'</code>
It will do its job and then export the private key and certificate (both as .pem and as .crt)

<hr>
<u>Generating a certificate in that CA</u>
This is the syntax for generating a certificate within your CA

<code>python3 generate_cert_with_authority.py <domain_name></code>

Now let's create a certificate for example.com
<code>python3 generate_cert_with_authority.py 'example.com'</code>

You now have these files: ca_cert.pem, ca_cert.crt, ca_cert.crt, github.com.crt, github.com.pem, github.com_key.pem.
If you do not, something has gone wrong.
<hr>
<br>
<u>Import your certificate into your computer</u>
Use the <code>import_cert_windows.py</code> script for Windows - for Linux, please use Google to help you - all distros are somewhat different, and the process will not be the same.
<h3>DISCLAIMER: The certificate you need to import is your CA cert - if you import the certficate for the individual website - it will not function properly.</h3>

<hr>
Upcoming updates
- Allow users to specify how long certificate should be issued for.
