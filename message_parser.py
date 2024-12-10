def msg_microparser(msg_micro):
    micro_res_list = []
    if msg_micro['attachments']:
        for i in msg_micro['attachments']:
            if "photo" in i.keys():
                micro_res_list.append(i["photo"]['orig_photo']['url'])
            elif "doc" in i.keys():
                micro_res_list.append(i["doc"]['url'])
            elif "audio" in i.keys():
                micro_res_list.append(i["audio"]['url'])
    if msg_micro["text"]:
        micro_res_list.append(msg_micro["text"])
    return micro_res_list


def message_parser(msg):
    try:
        # peer_id - id чата в Сферум
        res_list = []
        print(msg)
        res_list.extend(msg_microparser(msg))

            # пересланные
        if 'fwd_messages' in msg.keys():
            for i in msg["fwd_messages"]:
                print(i)
                res_list.extend(msg_microparser(i))

        return res_list
    except Exception as x:
        print(x)
        return res_list
