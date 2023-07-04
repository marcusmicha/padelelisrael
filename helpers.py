def pretty_availabilities(availabilities:str) -> str:
    res = ''
    for date in availabilities:
        res += f'__{date}__\n'
        for club in availabilities[date]:
            res += f'\t\t_{club}_\n'
            for field in availabilities[date][club]:
                res += f'\t\t\t\t*{field}*\n'
                res += f'\t\t\t\t\t\tAvailabilities between\n'
                for av in availabilities[date][club][field]:
                    res += f'\t\t\t\t\t\t{av["av_start"]} and {av["av_end"]}\n'
            
    res = res.replace('-',' ')
    return res