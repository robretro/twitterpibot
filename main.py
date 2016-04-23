from identities import AndrewTathamIdentity, AndrewTathamPiIdentity, AndrewTathamPi2Identity, NumberwangHostIdentity, \
    JulieNumberwangIdentity, SimonNumberwangIdentity, EggPunBotIdentity, WhenIsInternationalMensDayBotIdentity, \
    BotgleArtistIdentity, TheMachinesCodeIdentity
from twitterpibot import hardware

if __name__ == '__main__':
    from twitterpibot.logic import fsh
    from twitterpibot.data_access import dal

    dal.export_tokens(fsh.root + "tokens.csv")

if __name__ == "__main__":
    import twitterpibot.bootstrap

    andrewtatham = AndrewTathamIdentity()
    andrewtathampi = AndrewTathamPiIdentity(andrewtatham)
    andrewtathampi2 = AndrewTathamPi2Identity(andrewtatham)

    andrewtatham.followers = [andrewtathampi, andrewtathampi2]
    andrewtathampi.converse_with = andrewtathampi2
    andrewtathampi2.converse_with = andrewtathampi

    numberwang_host = NumberwangHostIdentity(andrewtatham)
    julienumberwang = JulieNumberwangIdentity(andrewtatham)
    simonnumberwang = SimonNumberwangIdentity(andrewtatham)



    numberwang_host.contestants = [
        [julienumberwang, simonnumberwang],
        [julienumberwang, simonnumberwang],
        [julienumberwang, simonnumberwang],
        [andrewtatham, julienumberwang],
        [andrewtatham, simonnumberwang],
        [andrewtatham, andrewtathampi],
        [andrewtatham, andrewtathampi2],
        [andrewtathampi, andrewtathampi2]
    ]

    eggpunbot = EggPunBotIdentity(andrewtatham)
    whenmensday = WhenIsInternationalMensDayBotIdentity(andrewtatham)
    botgleartist = BotgleArtistIdentity(andrewtatham)

    themachinescode = TheMachinesCodeIdentity(andrewtatham)


    if hardware.is_raspberry_pi_2:
        all_identities = [
            andrewtatham,
            andrewtathampi,
            andrewtathampi2,
            numberwang_host,
            julienumberwang,
            simonnumberwang,
            eggpunbot,
            whenmensday,
            botgleartist,
            themachinescode
        ]
    else:
        all_identities = [
            andrewtatham,
            andrewtathampi,
            andrewtathampi2,
            # numberwang_host,
            # julienumberwang,
            # simonnumberwang,
            # eggpunbot,
            # whenmensday,
            # botgleartist,
            themachinescode
        ]

    twitterpibot.bootstrap.run(all_identities)
