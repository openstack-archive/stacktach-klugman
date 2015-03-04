klugman
=======

Python library and cmdline tools for accessing Quincy.


Examples:

```
$ klugman 
Usage:
  klugman.py [options] <command> [<args>...]
  klugman.py (-h | --help)
  klugman.py --version


$ klugman -h
Klugman - cmdline and client library for StackTach.v3

Usage:
  klugman.py [options] <command> [<args>...]
  klugman.py (-h | --help)
  klugman.py --version

Options:
  -h --help     Show this help message
  --version     Show klugman version
  --debug       Debug mode
  -a, --api_version <api_version>
                Which API version to use [default: latest]
  --url <url>   StackTach.v3 server url [default: http://localhost:8000]

For a list of possible StackTach commands, use:
   klugman help


$ klugman help
Klugman - StackTach.v3 client

Usage:
   klugman.py [options] streams [<args>...]
   klugman.py num-streams [<args>...] [options]
   klugman.py [options] archives [<args>...]

Options:
   -h, --help  show command options


$ klugman num-streams
+----------+-------+
| Property | Value |
+----------+-------+
|  count   |   19  |
+----------+-------+

$ klugman num-streams --state completed
+----------+-------+
| Property | Value |
+----------+-------+
|  count   |   4   |
+----------+-------+

$ klugman num-streams --state active
+----------+-------+
| Property | Value |
+----------+-------+
|  count   |   15  |
+----------+-------+

$ klugman streams -h
usage:
        klugman.py streams [options]

      options:
      --id <id>
                get stream with id
      --details
                return events with each stream
      --state <state>
                return streams in state
      --older_than <datetime>
                list streams where first_event < <datetime>
      --younger_than <datetime>
                list streams where last_event > <datetime>
      --trigger_name <name>
                list streams with given trigger definition
      --distinguishing_traits <dtraits>
                list stream with specific distriquishing traits

      Stream states:
      collecting - collecting events
      ready - ready for processing
      triggered - being processed
      processed - processing completed
      error - pipeline processing failed
      commit_error - pipeline result commit failed

      Distinguishing trait format:
      "trait:value;trait:value;..."


$ klugman streams
+-----------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|        Property       |                                                                                Value                                                                                |
+-----------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|           id          |                                                                                  17                                                                                 |
|         state         |                                                                              completed                                                                              |
|          name         |                                                                             test_trigger                                                                            |
|      first_event      |                                                                      2015-01-31 13:21:50.679800                                                                     |
|       last_event      |                                                                      2015-01-31 13:36:46.981800                                                                     |
|     fire_timestamp    |                                                                      2015-01-30 18:52:03.196602                                                                     |
|    expire_timestamp   |                                                                      2015-01-31 14:36:46.981800                                                                     |
| distinguishing_traits | {u'instance_id': u'bd8b66f6-745b-45ce-b9c2-43010f8d9cdf', u'timestamp': TimeRange from datetime.datetime(2015, 1, 31, 0, 0) to datetime.datetime(2015, 2, 1, 0, 0)} |
|         events        |                                                                                 None                                                                                |
+-----------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+

$ klugman streams --distinguishing_traits instance_id:1438620b-e426-4911-81cd-e5f82219a390
...


$ klugman streams --older_than 01-31-2015T13:30
...

$ klugman streams --older_than 01-31-2015T13:30 --state completed
...

$ klugman events --traits=os_distro:com.redhat
+--------------------+------------------------------------------+
|      Property      |                  Value                   |
+--------------------+------------------------------------------+
|       _mark        |                    1                     |
|    bandwidth_in    |                  537783                  |
|   bandwidth_out    |                 19189871                 |
|      disk_gb       |                   160                    |
|    display_name    |             Instance_296624              |
|    ephemeral_gb    |                    0                     |
|     event_type     |         compute.instance.update          |
|  instance_flavor   |          4GB Standard Instance           |
| instance_flavor_id |                    5                     |
|    instance_id     |   60c52a73-ec8e-47bc-81eb-eee38931a60e   |
|   instance_type    |          4GB Standard Instance           |
|    launched_at     |        2014-04-17 11:40:15.321940        |
|     memory_mb      |                   4096                   |
|     message_id     |   8eca72ba-3adb-4354-aaa4-f61980549e07   |
|  os_architecture   |                   x64                    |
|     os_distro      |                com.redhat                |
|     os_version     |                   6.3                    |
|     request_id     | req-511c28a6-c6ec-4173-a124-7c92989e443c |
|      root_gb       |                   160                    |
|      service       |             publisher-189550             |
|       state        |                  active                  |
| state_description  |               powering-off               |
|     tenant_id      |                  854126                  |
|     timestamp      |        2015-03-03 20:13:56.560940        |
|      user_id       |                  366869                  |
|       vcpus        |                    2                     |
+--------------------+------------------------------------------+

$ klugman events --msg_id=8eca72ba-3adb-4354-aaa4-f61980549e07
...


$ klugman events --name=compute.instance.power_off.end
...

$ klugman events --from="2015-03-04T22:25" --to="2015-03-04T22:45"

```
