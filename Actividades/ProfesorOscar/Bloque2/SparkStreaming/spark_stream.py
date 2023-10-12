r"""
 Counts words in UTF8 encoded, '\n' delimited text received from the network.
 Usage: structured_network_wordcount.py <hostname> <port>
   <hostname> and <port> describe the TCP server that Structured Streaming
   would connect to receive data.

 To run this on your local machine, you need to first run a Netcat server
    `$ nc -lk 9999`
 and then run the example
    `$ python structured_network_wordcount.py
    localhost 9999`
"""
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
#from pyspark.sql import SparkSession
#from pyspark.sql.functions import explode
#from pyspark.sql.functions import split

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: structured_network_wordcount.py <hostname> <port>", file=sys.stderr)
        sys.exit(-1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    #spark = SparkSession.builder.appName("StructuredNetworkWordCount").getOrCreate()  ##Session usually more DatraFrame oriented

    sc= SparkContext('local[2]', 'network word count')
    # BATCH INTERVAL
    ssc= StreamingContext(sc,10)     
    lines = ssc.socketTextStream(host,port)
    # Split each line into words



    words= lines.flatMap(lambda line: line.split(' ') )
    pairs = words.map(lambda word: (word,1 ))

    # Generate running word count
    wordCounts= pairs.reduceByKey(lambda x,y:x+y)
    wordCounts.pprint()

    
    ssc.start()
    ssc.awaitTermination()
    