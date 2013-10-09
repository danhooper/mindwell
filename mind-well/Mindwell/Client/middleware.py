import view_common


class AuthorizedUserMiddleware(object):
    def process_request(self, request):
        excluded_urls = ['UserNotAllowed', 'administrator']
        for excluded_url in excluded_urls:
            if excluded_url in request.path:
                return None
        if view_common.CheckUserNotAllowed():
            return view_common.CheckUserNotAllowed()
