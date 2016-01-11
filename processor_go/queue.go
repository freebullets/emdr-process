MsgChan chan Msg

func ProcessMsg() {
    select {
    case msg := <-MsgChan:
        // decompress message
        // call orders or history processor
    }
}

for int i := 0; i < 2; i++ {
    go ProcessMsg()
}

func main() {
    while msg := getMsg() {
        MsgChan <- msg
    }
}
//tcp://relay-us-central-1.eve-emdr.com:8050
