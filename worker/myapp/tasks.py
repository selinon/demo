#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ######################################################################
# Copyright (C) 2016-2017  Fridolin Pokorny, fridolin.pokorny@gmail.com
# This file is part of Selinon project.
# ######################################################################

from selinon import SelinonTask


class HelloTask(SelinonTask):
    def run(self, node_args):
        """ A simple hello world """
        if 'name' not in node_args.keys():
            raise ValueError("Please provide your name!")
        return {"result": "Hello, {}!".format(node_args['name'])}


class FibonacciTask(SelinonTask):
    def run(self, node_args):
        """ Counting N+1 item in Fibonacci sequence

        :param node_args: count (referring to N+1) how many times should be recursion done
        :return: dict, previous - result of the previous task,
                       me - sum of previous tasks,
                       count - current recursion count
        """
        if self.task_name in self.parent:
            parent_result = self.parent_task_result(self.task_name)
            return {
                'previous': parent_result['me'],
                'me': parent_result['previous'] + parent_result['me'],
                'count': parent_result['count'] - 1
            }
        else:
            return {
                'previous': 0,
                'me': 1,
                'count': node_args['count']
            }
