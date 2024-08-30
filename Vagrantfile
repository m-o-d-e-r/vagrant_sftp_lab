# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

#ENV['VAGRANT_DEFAULT_PROVIDER'] = 'libvirt'

Vagrant.configure("2") do |config|
  config.vm.box = "generic/ubuntu1804"

  ip_list = [
    "192.168.33.201",
    "192.168.33.202",
    "192.168.33.203",
  ]

  ip_list.each.with_index(1) do |ip_item, i|
    config.vm.define "sftp#{i}" do |server|
      server.vm.provider :libvirt do |libvirt|
        libvirt.cpus = 2
        libvirt.memory = "2048"
      end

      server.vm.hostname = "sftp#{i}"

      server.vm.network "private_network", ip: ip_item, dev: "br0"

      server.vm.provision "shell", path: "./scripts/provision.sh"
      server.vm.provision "file", source: "./scripts/cron_files.sh", destination: "./cron_files.sh"
      server.vm.provision "shell", inline: "mv ./cron_files.sh /home/admin/cron_files.sh"

      server.vm.provision "file", source: "./scripts/generate_raw_report.sh", destination: "./generate_raw_report.sh"
      server.vm.provision "shell", inline: "mv ./generate_raw_report.sh /home/admin/generate_raw_report.sh"

      server.vm.provision "shell" do |s|
        other_ips = ip_list.reject { |vm_ip| vm_ip == ip_item }.join('\\n')

        s.inline = <<-SHELL
          echo -e "#{other_ips}" > /home/admin/vms_ip
        SHELL
      end

      server.vm.provision "shell", path: "./scripts/receive_certs.sh"
      server.vm.provision "shell", path: "./scripts/post_provision.sh"

    end
  end
end
