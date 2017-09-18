import os

import testinfra.utils.ansible_runner
import lxml.html

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'

def test_openscap_compliance(host):

    oscap_run = host.run("oscap xccdf eval --profile xccdf_org.ssgproject.content_profile_stig-rhel7-disa --results scan-xccdf-centos7-stig-sida_after.xml --report /tmp/centos7-disa-stig-report_after.html /usr/share/xml/scap/ssg/content/ssg-centos7-ds.xml")

    with open('/tmp/centos7-disa-stig-report_after.html') as f:
        html = lxml.html.parse(f)
        oscap_results_preparsed = html.xpath('//*[@id="compliance-and-scoring"]/div[2]/div[2]/text()')
        oscap_results = oscap_results_preparsed[0].split(' ')[0]

    assert oscap_results == '35'



