import json
import os
import sys

# transforms

metadata_defaults = {
    "activityId": "",
    "additionalContext": {
        "ansibleFileType": "",
        "playbookContext": {},
        "roleContext": {}
    },
    "documentUri": "",
}

def main():
    for line in sys.stdin:
        event = json.loads(line)
        # === GENERIC
        #  - remove integrations
        del event['integrations']

        # === COMPLETION
        if event['event'] == "completion":
            #  - properties.request.prompt must be a string
            if type(event['properties']['request']['prompt']) != str:
                event['properties']['request']['prompt'] = ""
            # - fix metadata
            try:
                del event['properties']['metadata']['additionalContext']
            except:
                ...
        # === ATTRIBUTION
        elif event['event'] == "attribution":
            if 'attributions' not in event['properties']:
                attribution = {}
                for x in ('ansible_type', 'data_source', 'path', 'repo_name', 'repo_url', 'score', 'license'):
                    attribution[x] = event['properties'][x]
                    del event['properties'][x]
                event['properties']['attributions'] = [attribution]

        elif event['event'] == "inlineSuggestionFeedback":
            if type(event['properties']['exception']) != str:
                event['properties']['exception'] = ""


        print(json.dumps(event))

if __name__ =="__main__":
    main()