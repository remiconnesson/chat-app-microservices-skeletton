FROM golang:1.19-alpine as builder

WORKDIR /app

COPY ./go.mod ./go.sum ./

RUN go mod download

COPY ./main.go .

RUN CGO_ENABLED=0 go build -o spaServer .

RUN chmod +x /app/spaServer

FROM alpine:latest

WORKDIR /app

COPY --from=builder /app/spaServer .

COPY ./www/dist ./www/dist

EXPOSE 80

CMD ["/app/spaServer"]
