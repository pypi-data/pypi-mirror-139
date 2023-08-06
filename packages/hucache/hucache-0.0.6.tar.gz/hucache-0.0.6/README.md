## hucache
A Declarative Caching Library for Human

## Usage

```
@cache("experiment_id:{experiment_id}:version:{version_list}", timeout=600)
def get_variants_by_experiment_id(self, session, experiment_id, version_list):
    pass
```
