def run():
    print("I'm starting !")
    import upload
    import datetime
    import Create_video
    Create_video.create()
    d = datetime.datetime.today()
    while d.weekday() != 5:
        d += datetime.timedelta(1)
    upload.send(d)
    print('finished')


def lunch_all(d=None):
    from datetime import datetime, timedelta
    import time

    if d is None:
        d = datetime.today()
    while d.weekday() != 2:
        d += timedelta(1)

    x = datetime.today()
    y = d.replace(day=d.day, hour=12, minute=0, second=0, microsecond=0)
    delta_t = y - x
    print("Next start :", y)

    secs = delta_t.seconds + 1

    time.sleep(secs)

    run()

    time.sleep(timedelta(1).seconds)


if __name__ == '__main__':
    while True:
        lunch_all()
