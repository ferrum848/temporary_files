import grpc
from concurrent import futures
import time

# import the generated classes
import wand_pb2
import wand_pb2_grpc

# import the original calculator.py
import main_function

# create a class to define the server functions, derived from
# calculator_pb2_grpc.CalculatorServicer
class magic_wandServicer(wand_pb2_grpc.magic_wandServicer):

    # calculator.square_root is exposed here
    # the request and response are of the data type
    # calculator_pb2.Number
    def find_mask(self, request, context):
        response = wand_pb2.ResultMask()
        response.image, response.mask = main_function.main_function(request.image, request.x, request.y, request.wand, request.antialiasing, request.edges, request.threshold, request.mode, request.criterion, request.shape0, request.shape1, request.shape2, request.mask)
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_CalculatorServicer_to_server`
# to add the defined class to the server
wand_pb2_grpc.add_magic_wandServicer_to_server(
        magic_wandServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)