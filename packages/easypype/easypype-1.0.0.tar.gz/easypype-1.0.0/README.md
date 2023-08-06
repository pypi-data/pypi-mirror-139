# EasyPype - Create a flexible, extensible, potent ETL
 ---
EasyPype allows you to create flexible and extensible ELTs using python. You can setup the sequence of operations you need and sink all data processed easily. Also, you may use the tools provided to create variations of the same pipe, with some minor changes.

# Overview
 ---
EasyPype will offer you:

  - Easy and flexibe way to define a set of instructions (extract, load or transform) and the correct order to execute them.
  - Multiprocessing execution of your instructions.
  - Extensible code, so you can add whatever new features easily.


## Quick start
---
To get started, you must first install EasyPype:
```
pip install easypype
```

Then, create a empty python file and import it:
```
import easypype as ep
```

In order to understand how EasyPype will help you, let's take a look at this code snippet:
```
import easypype as ep

pipe = ep.PipeBuilderConcrete().command(ep.Sum(2)).build()
mySink = ep.ConcreteSink()
mySink.collect([1, 2, 3])
pipe.do(mySink)
print(mySink.data)
```

Basically, EasyPype uses four components:
    1. PipeBuilderConcrete, It's an object that create a configured Pipe, according to the commands set.
    2. ConcreteSink, It's the entity that will hold the information across multiple executions.
    3. Pipe, It executes all the logic you've defined. All results are stored in your ConcreteSink object.
    4. Command, It's the instruction you want execute. In this case, an instruction Sum was used to sum each value of the list by two.
    
Hence, you can:
- Load data
```
mySink = ep.ConcreteSink()
mySink.collect([1, 2, 3])
```
- Setup instructions
```
pipe = ep.PipeBuilderConcrete().command(ep.Sum(2)).build()
```
- Run pipeline
```
pipe.do(mySink)
```

### Adding custom commands
By default, EasyPype has a command called Sum that iterates an iterable entity and increases each register by some amount. However, you can easily define your own commands:
```
import easypype as ep

class Multiplier(ep.Command):

    def __init__(self, amount):
        self.amount = amount

    def multiply(self, sink: ep.Sink):
        return [i + self.amount for i in sink.data]

    def do(self, sink: ep.Sink):
        return self.multiply(sink)
        
pipe = ep.PipeBuilderConcrete().command(Multiplier(2)).build()
mySink = ep.ConcreteSink()
mySink.collect([1, 2, 3])
pipe.do(mySink)
print(mySink.data)
```

Commands only need three things:
1. Extends Command class.
2. Implement do(self, sink: ep.Sink).
3. Write your operation.
4. Return the data loaded or transformed. (It will be collected by the Sink)

Keep in mind that Commands could also include data loading from databases, data exporting, data visualization and so on... The main point is, If you've implemented the Command correctly, It can be used along with any other Command easily.
