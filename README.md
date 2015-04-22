klugman
=======

Python library and cmdline tools for accessing Quincy.

Using Klugman as a client library:

```
from klugman import v1

events = v1.Events('http://www.example.com:8000')
data = events.get_events_count(name='compute.instance.update')

streams = v1.Streams('http://www.example.com:8000')
data = streams.get_streams(state='completed', details=True)
```

Command-line Examples:

```
$ klugman http://127.0.0.1 streams -h
usage: klugman url streams [-h] [--name trigger_name] [--from datetime]
                           [--to datetime] [--traits trait_list] [--details]
                           [--state {active,firing,expiring,error,expire_error,completed,retry_fire,retry_expire}]
                           [--count | --id stream_id]

optional arguments:
  -h, --help            show this help message and exit
  --name trigger_name   Return streams of type trigger_name.
  --from datetime       Return streams last updated after datetime
  --to datetime         Return streams last updated before datetime
  --traits trait_list   Return streams with specific distinguishing traits.
  --details             Return full event details.
  --state {active,firing,expiring,error,expire_error,completed,retry_fire,retry_expire}
                        Only return streams in this state.
  --count               Return a count of streams matching filter criteria.
  --id stream_id        Return a single specific stream by id.

$ klugman http://stacktach3-api01.example.com:8000 streams --count
+----------+-------+
| Property | Value |
+----------+-------+
|  count   | 44216 |
+----------+-------+

$ klugman http://stacktach3-api01.example.com:8000 streams --count --state completed
+----------+-------+
| Property | Value |
+----------+-------+
|  count   | 42571 |
+----------+-------+


$ klugman http://stacktach3-api01.example.com:8000 streams
+---------+------------------+---------------------------------------------------------------------------------------------+
| Section |     Property     |                                            Value                                            |
+---------+------------------+---------------------------------------------------------------------------------------------+
|  Stream |        id        |                                            44171                                            |
|  Stream |      state       |                                            active                                           |
|  Stream |       name       |                                         test_trigger                                        |
|  Stream |   first_event    |                                  2015-04-22 21:06:09.400561                                 |
|  Stream |    last_event    |                                  2015-04-22 21:07:17.317974                                 |
|  Stream |  fire_timestamp  |                                             None                                            |
|  Stream | expire_timestamp |                                  2015-04-24 21:07:17.317974                                 |
| D.Trait |   instance_id    |                             3ed27346-5906-4790-9b6e-e095e5b0cfa4                            |
| D.Trait |    timestamp     | TimeRange from datetime.datetime(2015, 4, 22, 0, 0) to datetime.datetime(2015, 4, 23, 0, 0) |
+---------+------------------+---------------------------------------------------------------------------------------------+

$ klugman http://stacktach3-api01.example.com:8000 streams --id 44171 --detail
+---------+------------------+---------------------------------------------------------------------------------------------+
| Section |     Property     |                                            Value                                            |
+---------+------------------+---------------------------------------------------------------------------------------------+
|  Stream |        id        |                                            44171                                            |
|  Stream |      state       |                                            active                                           |
|  Stream |       name       |                                         test_trigger                                        |
|  Stream |   first_event    |                                  2015-04-22 21:06:09.400561                                 |
|  Stream |    last_event    |                                  2015-04-22 21:15:05.962515                                 |
|  Stream |  fire_timestamp  |                                             None                                            |
|  Stream | expire_timestamp |                                  2015-04-24 21:15:05.962515                                 |
| D.Trait |   instance_id    |                             3ed12384-5906-4790-9b6e-e095e5b0cfa4                            |
| D.Trait |    timestamp     | TimeRange from datetime.datetime(2015, 4, 22, 0, 0) to datetime.datetime(2015, 4, 23, 0, 0) |
+---------+------------------+---------------------------------------------------------------------------------------------+
Events:
+--------------------+------------------------------------------+
|      Property      |                  Value                   |
+--------------------+------------------------------------------+
|      disk_gb       |                    40                    |
|    display_name    |              my_ubuntu1404               |
|    ephemeral_gb    |                    0                     |
|     event_type     |         compute.instance.update          |
|        host        |           nova-api05.example.com         |
|  instance_flavor   |          1GB Standard Instance           |
| instance_flavor_id |                    3                     |
|    instance_id     |   3ed23782-5906-4790-9b6e-e095e5b0cfa4   |
|   instance_type    |          1GB Standard Instance           |
|     memory_mb      |                   1024                   |
|     message_id     |   a58e25ed-01f3-42d8-8979-5f1603ab2468   |
|  os_architecture   |                   x64                    |
|     os_distro      |                com.ubuntu                |
|     os_version     |                  14.04                   |
|     request_id     | req-758de1f9-03e9-4337-af7d-d9efe3efc730 |
|      root_gb       |                    40                    |
|      service       |                   api                    |
|       state        |                 building                 |
| state_description  |                scheduling                |
|     tenant_id      |                  1234                    |
|     timestamp      |        2015-04-22 21:06:09.400561        |
|      user_id       |                  4567                    |
|       vcpus        |                    1                     |
+--------------------+------------------------------------------+
+--------------------+------------------------------------------+
|      Property      |                  Value                   |
+--------------------+------------------------------------------+
|      disk_gb       |                    40                    |
|    display_name    |              my_ubuntu1404               |
|    ephemeral_gb    |                    0                     |
|     event_type     |         compute.instance.update          |
|        host        |               c-88-77-44-2               |
|  instance_flavor   |          1GB Standard Instance           |
| instance_flavor_id |                    3                     |
|    instance_id     |   3ed23782-5906-4790-9b6e-e095e5b0cfa4   |
|   instance_type    |          1GB Standard Instance           |
|     memory_mb      |                   1024                   |
|     message_id     |   dbb6a5c0-08b8-45c8-85b4-a77b2b876bc3   |
|  os_architecture   |                   x64                    |
|     os_distro      |                com.ubuntu                |
|     os_version     |                  14.04                   |
|     request_id     | req-758de1f9-03e9-4337-af7d-d9efe3efc730 |
|      root_gb       |                    40                    |
|      service       |                   None                   |
|       state        |                 building                 |
| state_description  |                                          |
|     tenant_id      |                  1234                    |
|     timestamp      |        2015-04-22 21:06:09.888688        |
|      user_id       |                  4567                    |
|       vcpus        |                    1                     |
+--------------------+------------------------------------------+


$ klugman http://stacktach3-api01.example.com:8000 streams --traits instance_id:633fe23b-7c6a-dead-beef-55fcc6803cbc
+---------+------------------+---------------------------------------------------------------------------------------------+
| Section |     Property     |                                            Value                                            |
+---------+------------------+---------------------------------------------------------------------------------------------+
|  Stream |        id        |                                            43993                                            |
|  Stream |      state       |                                            active                                           |
|  Stream |       name       |                                         test_trigger                                        |
|  Stream |   first_event    |                                  2015-04-22 18:21:28.462931                                 |
|  Stream |    last_event    |                                  2015-04-22 18:21:28.462931                                 |
|  Stream |  fire_timestamp  |                                             None                                            |
|  Stream | expire_timestamp |                                  2015-04-24 18:21:28.462931                                 |
| D.Trait |   instance_id    |                             633fe23b-7c6a-dead-beef-55fcc6803cbc                            |
| D.Trait |    timestamp     | TimeRange from datetime.datetime(2015, 4, 22, 0, 0) to datetime.datetime(2015, 4, 23, 0, 0) |
+---------+------------------+---------------------------------------------------------------------------------------------+
+---------+------------------+---------------------------------------------------------------------------------------------+
| Section |     Property     |                                            Value                                            |
+---------+------------------+---------------------------------------------------------------------------------------------+
|  Stream |        id        |                                            43992                                            |
|  Stream |      state       |                                            active                                           |
|  Stream |       name       |                                         test_trigger                                        |
|  Stream |   first_event    |                                  2015-04-22 18:21:27.905027                                 |
|  Stream |    last_event    |                                  2015-04-22 18:24:18.985118                                 |
|  Stream |  fire_timestamp  |                                             None                                            |
|  Stream | expire_timestamp |                                  2015-04-24 18:24:18.985118                                 |
| D.Trait |   instance_id    |                             633fe23b-7c6a-dead-beef-55fcc6803cbc                            |
| D.Trait |    timestamp     | TimeRange from datetime.datetime(2015, 4, 22, 0, 0) to datetime.datetime(2015, 4, 23, 0, 0) |
+---------+------------------+---------------------------------------------------------------------------------------------+

$ klugman http://stacktach3-api01.example.com:8000 streams --state completed
+---------+------------------+---------------------------------------------------------------------------------------------+
| Section |     Property     |                                            Value                                            |
+---------+------------------+---------------------------------------------------------------------------------------------+
|  Stream |        id        |                                            43498                                            |
|  Stream |      state       |                                          completed                                          |
|  Stream |       name       |                                         test_trigger                                        |
|  Stream |   first_event    |                                  2015-04-20 00:00:18.740466                                 |
|  Stream |    last_event    |                                  2015-04-20 00:00:18.740466                                 |
|  Stream |  fire_timestamp  |                                  2015-04-22 11:53:37.441695                                 |
|  Stream | expire_timestamp |                                  2015-04-22 00:00:18.740466                                 |
| D.Trait |   instance_id    |                             7080633a-ffa3-dead-beef-d1549b4ac049                            |
| D.Trait |    timestamp     | TimeRange from datetime.datetime(2015, 4, 19, 0, 0) to datetime.datetime(2015, 4, 20, 0, 0) |
+---------+------------------+---------------------------------------------------------------------------------------------+

$ klugman http://127.0.0.1 events -husage: klugman url events [-h] [--name event_name] [--from datetime]
[--to datetime] [--traits trait_list]
[--count | --msg_id message_id]

optional arguments:
-h, --help           show this help message and exit
--name event_name    Return events of type event_name.
--from datetime      Return events generated before datetime
--to datetime        Return events generated after datetime
--traits trait_list  Return events with specific traits.
--count              Return a count of events matching filter criteria.
--msg_id message_id  Return a single specific event by message id.


$ klugman http://stacktach3-api01.example.com:8000 events 
+--------------------+------------------------------------------+
|      Property      |                  Value                   |
+--------------------+------------------------------------------+
|       _mark        |                  6544b                   |
|      disk_gb       |                    80                    |
|    display_name    |              My_Display_Name             |
|    ephemeral_gb    |                    0                     |
|     event_type     |         compute.instance.update          |
|        host        |              c-11-22-33-4                |
|  instance_flavor   |          2GB Standard Instance           |
| instance_flavor_id |                    4                     |
|    instance_id     |   85240caf-71cf-dead-beef-6735298e6090   |
|   instance_type    |          2GB Standard Instance           |
|     memory_mb      |                   2048                   |
|     message_id     |   c49d08be-dae5-4740-8f04-fb4cc27ac2fa   |
|  os_architecture   |                   x64                    |
|     os_distro      |                org.centos                |
|     os_version     |                    7                     |
|     request_id     | req-16b4995e-8a14-4b25-bd1c-ba68e82773f7 |
|      root_gb       |                    80                    |
|      service       |                   None                   |
|       state        |                 building                 |
| state_description  |                 spawning                 |
|     tenant_id      |                   725                    |
|     timestamp      |        2015-04-22 21:43:29.940846        |
|      user_id       |                   945                    |
|       vcpus        |                    2                     |
+--------------------+------------------------------------------+


$ klugman http://stacktach3-api01.example.com:8000 events --name compute.instance.create.end
+--------------------+------------------------------------------+
|      Property      |                  Value                   |
+--------------------+------------------------------------------+
|       _mark        |                  6547e                   |
|      disk_gb       |                    80                    |
|    display_name    |              My_Display_Name             |
|    ephemeral_gb    |                    0                     |
|     event_type     |       compute.instance.create.end        |
|        host        |              c-11-22-33-4                |
|  instance_flavor   |          2GB Standard Instance           |
| instance_flavor_id |                    4                     |
|    instance_id     |   0c30d4be-409d-dead-beef-6d8a3744e80f   |
|   instance_type    |          2GB Standard Instance           |
|    launched_at     |           2015-04-22 21:46:04            |
|     memory_mb      |                   2048                   |
|      message       |                 Success                  |
|     message_id     |   51bd735f-9817-4940-9826-5b057bf51f70   |
|  os_architecture   |                   x64                    |
|     os_distro      |           com.microsoft.server           |
|     os_version     |                  2012.0                  |
|    rax_options     |                    4                     |
|     request_id     | req-108e129d-49fd-1213-8e93-3f5595fd4d6c |
|      root_gb       |                    80                    |
|      service       |                 compute                  |
|       state        |                  active                  |
| state_description  |                                          |
|     tenant_id      |                    3334                  |
|     timestamp      |        2015-04-22 21:46:05.066171        |
|      user_id       |                   3848                   |
|       vcpus        |                    2                     |
+--------------------+------------------------------------------+


$ klugman http://stacktach3-api01.example.com:8000 events --name compute.instance.create.end --count
+----------+-------+
| Property | Value |
+----------+-------+
|  count   | 10280 |
+----------+-------+


$ klugman http://stacktach3-api01.example.com:8000 events --msg_id 047d9d5c-9190-4b85-9963-35d4cd095d07
+--------------------+------------------------------------------+
|      Property      |                  Value                   |
+--------------------+------------------------------------------+
|      disk_gb       |                    80                    |
|    display_name    |              My_Display_Name             |
|    ephemeral_gb    |                    0                     |
|     event_type     |       compute.instance.create.end        |
|        host        |              c-11-22-33-4                |
|  instance_flavor   |          2GB Standard Instance           |
| instance_flavor_id |                    4                     |
|    instance_id     |   b3c1be31-0ebe-4d6d-9663-b617eabac421   |
|   instance_type    |          2GB Standard Instance           |
|    launched_at     |           2015-04-22 18:02:03            |
|     memory_mb      |                   2048                   |
|      message       |                 Success                  |
|     message_id     |   047d9d5c-9190-4b85-9963-35d4cd095d07   |
|  os_architecture   |                   x64                    |
|     os_distro      |                org.debian                |
|     os_version     |                    7                     |
|    rax_options     |                    0                     |
|     request_id     | req-597b08a3-faef-425a-8f63-b91abcb1e1dd |
|      root_gb       |                    80                    |
|      service       |                 compute                  |
|       state        |                  active                  |
|     tenant_id      |                    3334                  |
|     timestamp      |        2015-04-22 21:46:05.066171        |
|      user_id       |                   3848                   |
|       vcpus        |                    2                     |
+--------------------+------------------------------------------+

```
