import os
import pytest
from PandorasLock import PandorasKey

@pytest.fixture
def pandoras_key_fixture():
    # Assuming the tests are run from the project root directory
    config_path = os.path.join(os.path.dirname(__file__), '..', 'PandorasLock', 'pandorasconfig.json')
    return PandorasKey(config_path)

def generic_sanitization_and_reverse(pandoras_key_fixture, test_text, expected_sanitized):
    # Test sanitization
    sanitized_text = pandoras_key_fixture.sanitize(test_text)
    assert sanitized_text == expected_sanitized

    # Test reverse-sanitization
    reversed_text = pandoras_key_fixture.reverse_sanitization(sanitized_text)
    assert reversed_text == test_text

def test_ip_address(pandoras_key_fixture):
    generic_sanitization_and_reverse(pandoras_key_fixture, "My IP is 192.168.1.1", "My IP is IP")

def test_cidr(pandoras_key_fixture):
    generic_sanitization_and_reverse(pandoras_key_fixture, "Network CIDR is 192.168.1.0/24", "Network CIDR is CIDR")

def test_ssn(pandoras_key_fixture):
    generic_sanitization_and_reverse(pandoras_key_fixture, "My SSN is 123-45-6789", "My SSN is S-S-N")

def test_awsArn(pandoras_key_fixture):
    generic_sanitization_and_reverse(pandoras_key_fixture, "My AWS account number is arn:aws:iam::123456789012", "My AWS account number is arn:aws:iam::arnAccountNum")

def test_awsVolId(pandoras_key_fixture):
    generic_sanitization_and_reverse(pandoras_key_fixture, "My volumeId is vol-12345678", "My volumeId is volumeId")

def test_sgID(pandoras_key_fixture):
    generic_sanitization_and_reverse(pandoras_key_fixture, "The Security group ID is sg-abcdefgh", "The Security group ID is securityGroupId")

def test_ec2ID(pandoras_key_fixture):
    generic_sanitization_and_reverse(pandoras_key_fixture, "Here is the AWS Arn for that EC2 instance arn:aws:ec2:region:123456789012:instance/i-ab365cdefgh", "Here is the AWS Arn for that EC2 instance arn:aws:ec2:region:arnAccountNum:instanceId")

def test_rdsID(pandoras_key_fixture):
    generic_sanitization_and_reverse(pandoras_key_fixture, "The RDS arn:aws:rds:region:123456789012:db:rds-db is down", "The RDS arn:aws:rds:region:arnAccountNum:db:rdsId is down")

def test_sanitize_and_reverse_complex(pandoras_key_fixture):
    test_text = "Sensitive info: 123-45-6789. Another ARN: arn:aws:lambda:us-east-1:016180545588:function:regionVisitor"
    expected_sanitized = "Sensitive info: S-S-N. Another ARN: arn:aws:lambda:us-east-1:arnAccountNum0:function:arnName0"
    sanitized_text = pandoras_key_fixture.sanitize(test_text)
    assert sanitized_text == expected_sanitized

    reversed_text = pandoras_key_fixture.reverse_sanitization(sanitized_text)
    assert reversed_text == test_text

def test_sanitize_no_match(pandoras_key_fixture):
    test_text = "No sensitive info here"
    sanitized_text = pandoras_key_fixture.sanitize(test_text)
    assert test_text == sanitized_text
