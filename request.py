import numpy as np

class Request(object):
    def __init__(self,                  # take request_1-2(2)-1(2) as an example  [r_1-1-1, r_1-1-2, r_1-2-1, r_1-2-2]
                 ids: list,             # [1, 2] [1, 2] [1, 2] [1, 2]
                 sub_requests: list,    # [2, 2]
                 audio_data: np.ndarray,
                 text_data: str,
                 signal: int,
                 start_time: float) -> None:
        self.ids = ids
        self.sub_requests = sub_requests
        self.audio_data = audio_data
        self.text_data = text_data
        self.signal = signal
        self.start_time = start_time

    def copy(self):
        return Request(ids=self.ids.copy(),
                       sub_requests=self.sub_requests.copy(),
                       audio_data=self.audio_data,
                       text_data=self.text_data,
                       signal=self.signal,
                       start_time=self.start_time)

