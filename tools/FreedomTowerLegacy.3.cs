// Optional GTA V Legacy helper. Requires Script Hook V and
// ScriptHookVDotNet v3.7.0-nightly.198 (or a compatible newer v3 build).
// Enables GTA Online map data locally in Story Mode; does not start GTA Online.
// Does not implement elevators, teleportation, or alter the player.
using System;
using GTA;
using GTA.Native;

public sealed class FreedomTowerLegacy : Script
{
    private bool started;

    public FreedomTowerLegacy()
    {
        Interval = 1000;
        Tick += OnTick;
    }

    private void OnTick(object sender, EventArgs e)
    {
        if (started || Function.Call<bool>(Hash.GET_IS_LOADING_SCREEN_ACTIVE))
            return;

        started = true;
        Tick -= OnTick;

        // These native calls reload map data and may block for several seconds.
        // CallLongBlockingFunc prevents SHVDN's normal script timeout.
        Function.CallLongBlockingFunc(Hash.ON_ENTER_MP);
        Function.CallLongBlockingFunc(Hash.SET_INSTANCE_PRIORITY_MODE, 1);

        foreach (string name in Maps)
            Function.Call(Hash.REQUEST_IPL, name);
    }

    private static readonly string[] Maps = {
        "one_wtc01",
        "one_wtc_pali",
        "one_wtc_plaza",
        "robbbs_wtc_appa2",
        "robbbs_wtc_appartment_01",
        "robbbs_wtc_appartment_03",
        "robbbs_wtc_appartment_04",
        "robbbs_wtc_buil_prop2",
        "robbbs_wtc_build_prop",
        "robbbs_wtc_emissive",
        "robbbs_wtc_hall_milo",
        "robbbs_wtc_office",
        "robbbs_wtc_office_02",
        "robbbs_wtc_plaza_acqua",
        "robbbs_wtc_plaza_prop",
        "robbs_wtc_office_03",
        "wtc_garage",
    };
}
