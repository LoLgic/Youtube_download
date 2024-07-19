class DownloadError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
        
        
#         **** ERROR ****      
#RegexMatchError: get_throttling_function_name: could not find match for multiple
#https://github.com/pytube/pytube/issues/1707