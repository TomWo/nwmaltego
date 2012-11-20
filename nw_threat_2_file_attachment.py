#!/usr/bin/env python
# Copyright (C) 2012 nwmaltego Developer.
# This file is part of nwmaltego - https://github.com/bostonlink/nwmaltego
# See the file 'LICENSE' for copying permission.

# Netwitness Threat to Filename Maltego transform
# Author: David Bressler (@bostonlink)

import sys
import urllib2, urllib, json

from lib import nwmodule

# Maltego XML Header
trans_header = """<MaltegoMessage>
<MaltegoTransformResponseMessage>
    <Entities>"""

# Authenticate to the NW Concentrator via HTTP basic auth

nwmodule.nw_http_auth()

# NW REST API Query amd results

threat_name = sys.argv[1]
fields = sys.argv[2].split('#')
parse = fields[1]
parse = parse.split('=')
ip = parse[1]

field_name = 'attachment'
where_clause = 'risk.warning="%s" && ip.src=%s || ip.dst=%s' % (threat_name, ip, ip)

ret_data = nwmodule.nwValue(0, 0, 20, field_name, 'application/json', where_clause)

json_data = json.loads(ret_data)
results_dic = json_data['results']
fields_list = results_dic['fields']
file_list = []

# Print the Maltego XML Header
print trans_header

# Logic to parse the NW data returned and craft the Maltego entities

for dic in fields_list:
    
    id1 = dic['id1']
    id2 = dic['id2']
    flags = dic['flags']
    value = dic['value']
    count = dic['count']
    type_d = dic['type']
    format_d = dic['format']
    
    if value in file_list:
	continue
    else:
	
	if value == '<none>':
            new_value = value.lstrip('<').rstrip('>')

            print """       <Entity Type="netwitness.NWFilename">
                <Value>%s</Value>
                <AdditionalFields>
                    <Field Name="risk" DisplayName="Threat Name">%s</Field>
                    <Field Name="ip" DisplayName="IP Address">%s</Field>
		    <Field Name="metaid1" DisplayName="Meta id1">%s</Field>
                    <Field Name="metaid2" DisplayName="Meta id2">%s</Field>
                    <Field Name="type" DisplayName="Type">%s</Field>
                    <Field Name="count" DisplayName="Count">%s</Field>
                </AdditionalFields> 
            </Entity>""" % (new_value, threat_name, ip, id1, id2, type_d, count)

        elif '&' in value:
            new_value = value.replace('&', '%amp;')

            print """       <Entity Type="netwitness.NWFilename">
                <Value>%s</Value>
                <AdditionalFields>
                    <Field Name="risk" DisplayName="Threat Name">%s</Field>
                    <Field Name="ip" DisplayName="IP Address">%s</Field>
		    <Field Name="metaid1" DisplayName="Meta id1">%s</Field>
                    <Field Name="Metaid2" DisplayName="Meta id2">%s</Field>
                    <Field Name="Type" DisplayName="Type">%s</Field>
                    <Field Name="Count" DisplayName="Count">%s</Field>
                </AdditionalFields> 
            </Entity>""" % (new_value, threat_name, ip, id1, id2, type_d, count)

        else:

            print """       <Entity Type="netwitness.NWFilename">
                <Value>%s</Value>
                <AdditionalFields>
                    <Field Name="risk" DisplayName="Threat Name">%s</Field>
		    <Field Name="ip" DisplayName="IP Address">%s</Field>
                    <Field Name="Metaid1" DisplayName="Meta id1">%s</Field>
                    <Field Name="Metaid2" DisplayName="Meta id2">%s</Field>
                    <Field Name="Type" DisplayName="Type">%s</Field>
                    <Field Name="Count" DisplayName="Count">%s</Field>
                </AdditionalFields> 
            </Entity>""" % (value, threat_name, ip, id1, id2, type_d, count)
    
    file_list.append(value)

# Maltego transform XML footer

trans_footer = """  </Entities>
</MaltegoTransformResponseMessage>
</MaltegoMessage> """

print trans_footer    

