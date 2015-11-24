from copy import deepcopy


def publish_requests_as_catalog(publish_requests):
    """
    Format the set of publish_requests in the format expected by the
    resource_catalog_json view.

    :param publish_requests: set of `PublishRequest`
    :type publish_requests: list

    :returns: dict
    """
    # Catalog will be of official resources by language, eg:
    # [ { title: Open Bible Story, slug: obs, languages: [] } ]
    catalog = []
    # langs will contain a list of languages for the catalog item, while
    # listing all of the versions for the language + resource type
    resource = {"title": None, "slug": None, "langs": []}
    languages = {}
    for pub_req in publish_requests:
        # If the resource type changes, copy the previous to the catalog,
        # set the new resource title, slug and reset langs
        if resource["title"] != pub_req.resource_type.long_name:
            if resource["title"] is not None:
                resource["langs"] = [
                    lang for code, lang in languages.items()
                ]
                catalog.append(deepcopy(resource))
            resource["title"] = pub_req.resource_type.long_name
            resource["slug"] = pub_req.resource_type.short_name
            resource["langs"] = []
        else:
            # If this is the newest published version, set the date
            # mod(ified), append current data as first of the ver(sion)s
            if pub_req.language.code not in languages.keys():
                languages[pub_req.language.code] = {
                    "lc": pub_req.language.code,
                    "mod": pub_req.created_at,
                    "vers": [pub_req.data, ],
                }
            else:
                # Append all other items to the vers list
                languages[pub_req.language.code]["vers"].append(
                    pub_req.data
                )
    if resource["title"] is not None:
        catalog.append(resource)

    return {"cat": catalog}
