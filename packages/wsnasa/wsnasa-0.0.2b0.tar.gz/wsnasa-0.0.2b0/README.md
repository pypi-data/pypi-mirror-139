# Library for use services of NASA


Install package
>pip install wsnasa  

After installed package need does settings it for work. 

>from wsnasa.config import Config  
>Config(token='TOKENNASA',storage=ClassStorage, connection_string='conn_str')  

ClassStorage - wsnasa.entity.storage*

## Token
Get keys can here https://api.nasa.gov/
or use DEMO_KEY  

## Storage
Class <Storage*> implementes rule stores caches
Has second of classes: StorageMemory, StorageDatabase.  
If need use another class for storage use for implement of the interface  <AbcStorage>

>from wsnasa.entity.abclass.abcstorage import AbcStorage



