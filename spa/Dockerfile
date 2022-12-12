#
# The goal of if this build is to create
# the executable binaries from the go source code
#
FROM golang:1.19-alpine as builder

WORKDIR /app

COPY ./go.mod ./go.sum ./

RUN go mod download

COPY ./main.go .

RUN CGO_ENABLED=0 go build -o spaServer .

# not sure if it's necessary, just to be sure
RUN chmod +x /app/spaServer

#
# MULTI-STAGE BUILD
# the second from is the one we want;
# the first will be discarded.
# this one will run the server built in the previous stage
#

FROM alpine:latest

WORKDIR /app

COPY --from=builder /app/spaServer .

# this where the frontfiles are built
COPY ./www/dist ./www/dist

# For traefik port discovery, don't remove
EXPOSE 80 

CMD ["/app/spaServer"]










