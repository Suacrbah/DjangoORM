用于记录每一个ORM 生成SQL的性能指标：

1）执行时间（Execution time）：即ORM执行查询、插入、更新、删除等操作所需的时间。
工具：python

2）内存占用（Memory usage）：ORM所占用的内存资源，包括连接池、对象池、缓存等。
工具：memory_profiler

3）并发性能（Concurrency performance）：ORM在高并发情况下的性能表现，包括并发连接数、线程池大小、锁竞争等。
工具：threading 或 multiprocessing

4）SQL质量（SQL quality）：ORM生成的SQL语句的质量，包括语句的优化、索引的使用等。
工具：查看生成的sql，可以通过explain sql等方式分析