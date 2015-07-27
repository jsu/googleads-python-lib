#!/usr/bin/python
#
# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example updates the bid of a placement.

To add a placement, run add_placements.py.

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

Tags: AdGroupCriterionService.mutate
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

from googleads import adwords


AD_GROUP_ID = 'INSERT_AD_GROUP_ID_HERE'
CRITERION_ID = 'INSERT_PLACEMENT_CRITERION_ID_HERE'


def main(client, ad_group_id, criterion_id):
  # Initialize appropriate service.
  ad_group_criterion_service = client.GetService(
      'AdGroupCriterionService', version='v201506')

  # Construct operations and update bids.
  operations = [{
      'operator': 'SET',
      'operand': {
          'xsi_type': 'BiddableAdGroupCriterion',
          'adGroupId': ad_group_id,
          'criterion': {
              'xsi_type': 'Placement',
              'id': criterion_id,
          },
          'biddingStrategyConfiguration': {
              'bids': [
                  {
                      'xsi_type': 'CpmBid',
                      'bid': {
                          'microAmount': '1000000'
                      },
                  }
              ]
          }
      }
  }]
  ad_group_criteria = ad_group_criterion_service.mutate(operations)

  # Display results.
  if 'value' in ad_group_criteria:
    for criterion in ad_group_criteria['value']:
      if criterion['criterion']['Criterion.Type'] == 'Keyword':
        print ('Ad group criterion with ad group id \'%s\' and criterion id '
               '\'%s\' had its bid set to \'%s\'.'
               % (criterion['adGroupId'], criterion['criterion']['id'],
                  criterion['bids']['maxCpc']['amount']['microAmount']))
  else:
    print 'No ad group criteria were updated.'


if __name__ == '__main__':
  # Initialize client object.
  adwords_client = adwords.AdWordsClient.LoadFromStorage()

  main(adwords_client, AD_GROUP_ID, CRITERION_ID)