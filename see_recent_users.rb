#!/usr/bin/env ruby
require 'set'
user_key_pairs = {}

File.open(ENV['HOME'] + '/.ssh/authorized_keys').each do |public_key|
  file_name = public_key.split(' ')[2] + '.pub_key'
  key_file = File.new(file_name, 'w')
  key_file.puts public_key
  key_file.close
  key_sig_user = `ssh-keygen -l -f #{file_name}`
  rsa_signature = key_sig_user.split(' ')[1]
  rsa_public_comment = key_sig_user.split(' ')[2]
  user_key_pairs[rsa_signature] = rsa_public_comment
  system("rm #{file_name}")
end

recent_logins = `sudo tail /var/log/auth.log -n 200 | grep RSA |
                 awk '\{print $16\}'`
signatures = recent_logins.split("\n")

puts signatures.uniq.map{|signature| user_key_pairs[signature]}.join(', ')