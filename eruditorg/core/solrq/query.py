# -*- coding: utf-8 -*-
import re

"""
This module defines the main Query class. It is used by the solrq.Search class
to provide filtering capabilities on a Solr index.
"""


class Q(object):
    AND = 'AND'
    OR = 'OR'
    default = AND

    def __init__(self, **params):
        self.params = params.copy()
        self.operator = self.default
        self.operands = []
        self.negated = False

    def _combine(self, other, operator):
        if not isinstance(other, Q):
            raise TypeError(other)
        obj = type(self)()
        obj.operator = operator
        obj.operands.append(self if self.operands else self.params)
        obj.operands.append(other if other.operands else other.params)
        return obj

    def _negate(self):
        self.negated = not self.negated

    def __or__(self, other):
        return self._combine(other, self.OR)

    def __and__(self, other):
        return self._combine(other, self.AND)

    def __invert__(self):
        obj = type(self)()
        obj.operator = self.AND
        obj.operands.append(self if self.operands else self.params)
        obj._negate()
        return obj


class Query(object):
    """
    A Query object used to apply filters to a given Solr search.
    """
    filters_mapping = {}
    extra_params = {}

    # thanks to https://github.com/swistakm/solrq
    ESCAPE_RE = re.compile(r'(?<!\\)(?P<char>[ &|+\\\-!(){}[\]*^"~?:])')

    def __init__(self, search, q='*:*', fq="*:*"):
        """ Search request to Solr.

        :arg search: `solrq.Search` instance to use
        :arg qs: a default Solr query string to use
        """
        self.search = search
        self._q = q
        self._fq = fq

    def _prepare_querystring(self, base_qs, *args, safe=False, **kwargs):
        # Inserts Q params if applicable
        qarg_qs = None
        for qarg in args:
            subqs = self._get_q_querystring(qarg, safe=safe)
            qarg_qs = ' AND '.join([qarg_qs, subqs]) if qarg_qs else subqs
        base_qs = '({0}) AND ({1})'.format(base_qs, qarg_qs) if qarg_qs else base_qs

        # Inserts kwargs params
        kwargs_qs = self._get_querystring_from_dict(kwargs, safe=safe)
        base_qs = '({0}) AND ({1})'.format(base_qs, kwargs_qs) if kwargs_qs else base_qs
        return base_qs

    def filter(self, *args, safe=False, **kwargs):
        """ Prepares the querystring used to perform a query.

        This method returns a new instance of Query that allows
        to add another filters to the initial querystring.
        """
        qs = self._prepare_querystring(self._q, *args, safe=safe, **kwargs)
        return self.__class__(self.search, q=qs, fq=self._fq)

    def filter_query(self, *args, safe=False, **kwargs):
        """" Prepare the querystring used to perform a filter query

        This method returns a new instance of Query that allows
        to add another filter to the initial querystring.
        """
        fq = self._prepare_querystring(self._fq, *args, safe=safe, **kwargs)
        return self.__class__(self.search, q=self._q, fq=fq)

    def _get_q_querystring(self, q, safe=False):
        subqs_list = []

        for qchild in q.operands:
            if isinstance(qchild, Q):
                subqs = self._get_q_querystring(qchild, safe=safe)
            else:
                subqs = self._get_querystring_from_dict(qchild, safe=safe)

            # Handles the case when the query is negated
            if q.negated:
                subqs = '*:* -{}'.format(subqs)

            if subqs is None:
                continue

            subqs = '({})'.format(subqs)
            subqs_list.append(subqs)

        if not len(subqs_list):
            return self._get_querystring_from_dict(q.params)
        return ' {} '.format(q.operator).join(subqs_list)

    def _get_querystring_from_dict(self, params_dict, safe=False, base_qs=None):
        qs = base_qs
        # Inserts kwargs params
        for k, v in params_dict.items():
            if not safe:
                v = self.ESCAPE_RE.sub(r'\\\g<char>', v)
            if k in self.search.filters_mapping:
                subqs = self.search.filters_mapping[k].format(**{k: v})
            else:
                subqs = '{0}:{1}'.format(k, v)
            qs = ' AND '.join([qs, subqs]) if qs else subqs
        return qs

    def get_results(self, **kwargs):
        """ Triggers the search and returns the results. """
        params = self.search.extra_params.copy()
        params.update(kwargs)
        params['fq'] = self._fq
        return self.search.client.search(self._q, **params)

    results = property(get_results)
