#!/usr/bin/env ruby
require 'set'
users = []
user_key_pairs = {}
File.open(ENV['HOME'] + "/.ssh/authorized_keys").each do |l|
  file_name = l.split(" ")[2]
  key_file = File.new("#{file_name}.pub_key", "w")
  key_file.puts l
  key_file.close
  key_sig_user = %x{ssh-keygen -l -f #{file_name}.pub_key}
  user_key_pairs[key_sig_user.split(" ")[1]] =  key_sig_user.split(" ")[2]
end
recent_logins = %x{sudo tail /var/log/auth.log -n 200 | grep RSA | awk '\{print $16\}'}
signatures = recent_logins.split("\n")
curr_users = Set.new
for signature in signatures
    curr_users.add(user_key_pairs[signature])
end
puts curr_users.to_a.join(', ')