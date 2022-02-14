#!/usr/bin/env python3
import sys
import os
import importlib
import argparse
from uuid import uuid1
from pprint import pprint

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase


class TestStatusMessage(LFCliBase):
    def __init__(self, host, port,
                 _deep_clean=False,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(host, port, _debug=_debug_on, _exit_on_fail=_exit_on_fail)
        self.exit_on_error = False
        self.status_msg_url = "/status-msg"
        self.session_url = None
        self.msg_count = 0
        self.deep_clean = _deep_clean
        self.check_connect()
        self.debug = _debug_on

    def build(self):
        """create a new session"""
        new_session = uuid1()
        self.session_url = "/status-msg/" + str(new_session)
        # print("----- ----- ----- ----- ----- PUT ----- ----- ----- ----- ----- ----- ")
        self.json_put(self.session_url, _data={})

        # we should see list of sessions
        try:
            # print("----- ----- ----- ----- ----- GET ----- ----- ----- ----- ----- ----- ")
            session_response = self.json_get(self.status_msg_url)
            if self.debug:
                pprint(session_response)
            if "sessions" not in session_response:
                print("----- ----- ----- ----- ----- BAD ----- ----- ----- ----- ----- ----- ")
                self._fail("response lacks sessions element")
            if len(session_response["sessions"]) < 2:
                self._fail("why do we have less than two sessions?")
            for session in session_response["sessions"]:
                # print("----- ----- ----- ----- ----- SESSION ----- ----- ----- ----- ----- ----- ")
                pprint(session)
            self._pass("session created")
        except ValueError as ve:
            print("----- ----- ----- ----- ----- what??? ----- ----- ----- ----- ----- ----- ")
            self._fail(ve)
        return

    def start(self):
        """
        create a series of messages
        :return: None
        """
        # print("----- ----- ----- ----- ----- START ----- %s ----- ----- ----- ----- ----- " % self.session_url)
        message_response = self.json_get(self.session_url)
        if self.debug:
            pprint(message_response)
        if message_response:
            if "empty" in message_response:
                self._pass("empty response, zero messages")
            elif "messages" in message_response:
                messages_a = message_response["messages"]
                if len(messages_a) > 0:
                    self._fail("we should have zero messages")

        for msg_num in (1, 2, 3, 4, 5):
            # print("----- ----- ----- ----- ----- ----- %s ----- ----- ----- ----- ----- " % msg_num)
            # print("session url: "+self.session_url)
            self.msg_count = msg_num
            self.json_post(self.session_url, {
                "key": "test_status_message.py",
                "content-type": "application/json",
                "message": "message %s" % msg_num
            })
            message_response = self.json_get(self.session_url)
            if message_response:
                if len(message_response["messages"]) != msg_num:
                    pprint(message_response)
                    self._fail("we should have %s messages" % msg_num)

        self._pass("created and listed %s messages counted" % msg_num)

    def stop(self):
        """
        make sure we read those messages
        :return: None
        """

        message_list_response = self.json_get(self.session_url)
        if message_list_response:
            if "empty" in message_list_response:
                self._fail("empty response, we expect 1 or more messages")
            msg_num = 0
            for message_o in message_list_response["messages"]:
                msg_url = message_o["_links"]
                print("Message url: " + msg_url)
                message_response = self.json_get(msg_url)
                if self.debug:
                    pprint(message_response)
                for content_o in message_response["messages"]:
                    msg_num += 1
                    print("id %s" % content_o["message_id"])
                    print("key %s" % content_o["message"]["key"])
                    print("content-type %s" % content_o["message"]["content-type"])
                    print("message %s" % content_o["message"]["message"])

            if msg_num != self.msg_count:
                self._fail("(stop) expected %s messages, saw %s" % (self.msg_count, msg_num))
            else:
                self._pass("saw correct number of messages")

    def cleanup(self):
        """delete messages and delete the session"""

        message_list_response = self.json_get(self.session_url)
        if message_list_response:
            if "empty" in message_list_response:
                self._fail("empty response, we expect 1 or more messages")
            last_link = ""
            msg_num = 0
            for message_o in message_list_response["messages"]:
                # print("Delete Message url: "+msg_url)
                last_link = message_o["_links"]
                msg_num += 1

            if msg_num != self.msg_count:
                self._fail("(cleanup) expected %s messages, saw %s" % (self.msg_count, msg_num))
            message_response = self.json_delete(last_link)
            if self.debug:
                pprint(message_response)

        # check message removal
        message_list_response = self.json_get(self.session_url)
        if message_list_response:
            msg_num = len(message_list_response["messages"])
            if msg_num != (self.msg_count - 1):
                self._fail("(cleanup) expected %s messages, saw %s" % ((self.msg_count - 1), msg_num))
            else:
                self._pass("(cleanup) messages decreased by one")

            all_url = self.session_url + "/all"
            message_response = self.json_delete(all_url)
            if self.debug:
                pprint(message_response)

            message_list_response = self.json_get(self.session_url)
            if self.debug:
                pprint(message_list_response)
            if "messages" in message_list_response:
                msg_num = len(message_list_response["messages"])
            elif "empty" in message_list_response:
                msg_num = 0

            if msg_num == 0:
                return "deleted all messages in session"
            else:
                self._fail("failed to delete all messages in session")

            if 'empty' in message_list_response.keys():
                if self.debug:
                    print("--- del -------------------- -------------------- --------------------")
                self.exit_on_error = False
                self.json_delete("%s/this" % self.session_url, debug_=False)
                if self.debug:
                    print("--- ~del -------------------- -------------------- --------------------")
            else:
                return 'ports deleted successfully'

        sessions_list_response = self.json_get("/status-msg")
        if self.debug:
            pprint(sessions_list_response)
        session_list = sessions_list_response["sessions"]
        counter = 0
        for session_o in session_list:
            if self.debug:
                print("session %s link %s " % (self.session_url, session_o["_links"]))
            if session_o["_links"] == self.session_url:
                counter += 1
                self._pass("session not deleted")
                break
        if counter == 0:
            self._fail("session incorrectly deleted")
        else:
            return "Sessions properly deleted"

        try:
            if self.debug:
                print("--- del -------------------- -------------------- --------------------")
            self.json_delete(self.session_url + "/this", debug_=False)
            if self.debug:
                print("--- ~del -------------------- -------------------- --------------------")
        except ValueError as ve:
            print(ve)

        sessions_list_response = self.json_get("/status-msg")
        if self.debug:
            pprint(sessions_list_response)
        session_list = sessions_list_response["sessions"]
        counter = 0
        for session_o in session_list:
            if session_o["_links"] == self.session_url:
                counter += 1
                self._fail("session not deleted: " + session_o["_links"])
                break
        if counter == 0:
            self._pass("session correctly deleted")

        # make sure we fail on removing session zero

        if not self.deep_clean:
            return True

        print("Deleting all sessions...")
        counter = 0
        for session_o in session_list:
            counter += 1
            self.json_delete(session_o["_links"] + "/all")
        print("cleaned %s sessions" % counter)
        counter = 0
        for session_o in session_list:
            if session_o["session-id"] == "0":
                continue
            counter += 1
            self.json_delete(session_o["_links"] + "/this")
        print("deleted %s sessions" % counter)


def main():
    parser = LFCliBase.create_bare_argparse(
        prog=__file__,
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        formatter_class=argparse.RawTextHelpFormatter,

        description="""
Test the status message passing functions of /status-msg:
- create a session: PUT /status-msg/<new-session-id>
- post message: POST /status-msg/<new-session-id>
- list sessions: GET /status-msg/
- list messages for session: GET /status-msg/<new-session-id>
- delete message: DELETE /status-msg/<new-session-id>/message-id
- delete session: DELETE /status-msg/<new-session-id>/this
- delete all messages in session: DELETE /status-msg/<new-session-id>/all

Example:
./test_status_msg.py
""")
    parser.add_argument('--action', default="run_test", help="""
Actions can be:
    run_test    : run a messaging test
    new         : create new session
    update      : add message to session, requires --session, --key, --message
    read        : read message(s) from session, requires --session
    list        : list messages from session
    delete      : delete message, all messages using session/all or session using session/this
""")
    parser.add_argument('--session', type=str, help='explicit session or session/message-id')
    parser.add_argument('--deep_clean', type=bool, help='remove all messages and all sessions')
    parser.add_argument('--key', type=str, help='how to key the message')
    parser.add_argument('--message', type=str, help='message to include')
    args = parser.parse_args()

    status_messages = TestStatusMessage(args.mgr,
                                        args.mgr_port,
                                        _debug_on=args.debug,
                                        _exit_on_error=False,
                                        _exit_on_fail=False)
    if args.action == "new":
        if args.session is not None:
            status_messages.json_put("/status-msg/" + args.session, {})
        else:
            a_uuid = uuid1()
            status_messages.json_put("/status-msg/" + str(a_uuid), {})
            print("created session /status-msg/" + str(a_uuid))
        return

    if args.action == "update":
        if args.session is None:
            print("requires --session")
            return
        if args.key is None:
            print("requires --key")
            return
        if args.message is None:
            print("requires --message")
            return
        status_messages.json_post("/status-msg/" + args.session, {
            "key": args.key,
            "content-type": "text/plain",
            "message": args.message
        })
        return

    if args.action == "list":
        if args.session is None:
            response_o = status_messages.json_get("/status-msg/")
            pprint(response_o["sessions"])
        else:
            response_o = status_messages.json_get("/status-msg/" + args.session)
            pprint(response_o["messages"])
        return

    if args.action == "read":
        if args.session is None:
            print("requires --session")
            return
        if args.key is None:
            print("requires --key")
            return
        response_o = status_messages.json_get("/status-msg/%s/%s" % (args.session, args.key))
        pprint(response_o)
        return

    if args.action == "delete":
        if args.session is None:
            print("requires --session")
            return
        response_o = status_messages.json_delete("/status-msg/" + args.session)
        pprint(response_o)
        return

    if args.action == "run_test":
        if args.deep_clean:
            status_messages.deep_clean = True
        status_messages.build()
        if not status_messages.passes():
            print(status_messages.get_fail_message())
            exit(1)
        status_messages.start()
        status_messages.stop()
        if not status_messages.passes():
            print(status_messages.get_fail_message())
            exit(1)
        status_messages.cleanup()
        if status_messages.passes():
            print("Full test passed, all messages read and cleaned up")
        exit(0)


if __name__ == "__main__":
    main()
