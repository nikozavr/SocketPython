import asyncio
import time
import queue

async def handle_echo(reader, writer):
    size = await reader.read(4)
    data = await reader.read(int.from_bytes(size, byteorder='little'))
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))
    global q
    q.put(message)

async def timer_work(loop):
    global q
    empty = 1
    while True:
        if q.empty():
            if empty > 0:
                print("Empty")
                empty = empty - 1
        else:
            empty = 1
            print(q.get())
        await asyncio.sleep(0.04, loop=loop)
    return True

q = queue.Queue()
loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 6060, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    timer_task = asyncio.ensure_future(timer_work(loop))
    loop.run_until_complete(asyncio.wait([timer_task]))
except KeyboardInterrupt:
    timer_task.cancel()

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
print("Server closed")
loop.close()