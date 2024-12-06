def msg_microparser(msg_micro):
    micro_res_list = []
    if msg_micro['attachments']:
        if "photo" in msg_micro['attachments'][0].keys():
            micro_res_list.append(msg_micro['attachments'][0]["photo"]['orig_photo']['url'])
        elif "doc" in msg_micro['attachments'][0].keys():
            micro_res_list.append(msg_micro['attachments'][0]["doc"]['url'])
        elif "audio" in msg_micro['attachments'][0].keys():
            micro_res_list.append(msg_micro['attachments'][0]["audio"]['url'])
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
