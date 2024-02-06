import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from PandorasLock import PandorasKey

# Get the absolute path to the pandorasconfig.json file
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'PandorasLock', 'pandorasconfig.json'))

# Initialize PandorasKey with the correct config path
pandoras_key = PandorasKey(config_path)

# Replace this with your actual text to sanitize
test_text = "I hope this email finds you well. I am writing to inform you about an incident that occurred today, which caused significant disruption to our AWS cloud operations. This morning, I logged into our AWS account (123456789012) to perform routine maintenance and updates. I noticed that our EC2 instance (arn:aws:ec2:region:123456789012:instance/i-ab365cdefgh) was not responding as expected. I attempted to SSH into the instance using the IP address 192.168.1.1, but I was unable to establish a connection. Upon further investigation, I discovered that the entire subnet (192.168.1.0/24) was experiencing connectivity issues. This was particularly concerning as our RDS database (arn:aws:rds:region:123456789012:db:rds-db) and Lambda function (arn:aws:lambda:us-east-1:016180545588:function:regionVisitor) also reside within this subnet. I then attempted to troubleshoot the issue by checking the security group (sg-abcdefgh) associated with the EC2 instance and the RDS database. However, I encountered an error message stating 'Ran out of time waiting for sg-abcdefgh IpPermissions' 4 . This was a clear indication that the security group was not updating as expected, which could have been the root cause of the connectivity issues. In the midst of this, I received an alert that our EBS volume (vol-12345678) was nearing its capacity limit. This was unexpected as our monitoring systems did not indicate any unusual data usage or storage patterns. I suspect this could be related to the connectivity issues we were experiencing. To make matters worse, I realized that I had mistakenly used a Social Security number (123-45-6789) instead of the AWS account number in one of my scripts. This error could have potentially exposed sensitive information, although I immediately corrected it upon discovery. In summary, today was a challenging day due to a series of unexpected issues with our AWS cloud operations. I am currently working on resolving these issues and implementing measures to prevent similar incidents in the future. I will keep you updated on the progress and I am confident that we will be able to restore normal operations soon. I apologize for any inconvenience caused and appreciate your understanding in this matter"

# Sanitize the text
sanitized_text = pandoras_key.sanitize(test_text)

# Print the sanitized text
print("Sanitized Text:\n", sanitized_text)

# Print the sanitization map
print("\nSanitization Map:\n", pandoras_key.sanitization_map)

# Reverse the sanitization
reversed_text = pandoras_key.reverse_sanitization(sanitized_text)

# Print the reversed (original) text
print("\nReversed (Original) Text:\n", reversed_text)
