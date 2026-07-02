@name lib/drv/consolescreen/v1/readme

#[ **** **** **** **** **
    Date: 2 September 2025
    Author: rs / STEAM_0:0:33005408 / 76561198026276544

    Notes on Console Screen Internals:

    Console Screens (CS) are "hi-speed" devices. As such, they have an internal memory which is accessible
    to Expression 2 via Wirelink. [0]
    
    The CS memory consists of 2 x 2048 cell buffers. [1] 
    
    The "front-buffer" (FB) is visible and immutable. "back-buffer" (BB) is invisible and mutable. [2]
    
    When register Clk [2047] transitions Hi-Lo or Lo-Hi, The front-buffer is overwritten by a clone of the back-buffer. [3]
    
    The digital screen displays the contents of Buffer #1 exclusively. Triggering a clone of Buffer #2
    overwriting Buffer #1

    Sources:    
    [0] https://web.archive.org/web/20160625182702/http://wiki.wiremod.com/wiki/Console_Screen
    [1] https://github.com/wiremod/wire/blob/118bacb458459eb9631dee8436bb0fc008393d26/lua/entities/gmod_wire_consolescreen/cl_init.lua#L74
    [2] https://github.com/wiremod/wire/blob/118bacb458459eb9631dee8436bb0fc008393d26/lua/entities/gmod_wire_consolescreen/cl_init.lua#L119
    [3] https://github.com/wiremod/wire/blob/118bacb458459eb9631dee8436bb0fc008393d26/lua/entities/gmod_wire_consolescreen/cl_init.lua#L267

** **** **** **** **** ]#

#[ **** **** **** **** **

https://github.com/wiremod/wire/blob/master/lua/entities/gmod_wire_consolescreen/cl_init.lua

From wire/lua/entities/gmod_wire_consolescreen/cl_init.lua:

function ENT:Initialize()
	self.Memory1 = {}
	self.Memory2 = {}
	for i = 0, 2047 do
		self.Memory1[i] = 0
	end

	-- Caching control:
	-- [2020] - Force cache refresh
	-- [2021] - Cached blocks size (up to 28, 0 if disabled)
	--
	-- Hardware image control:
	-- [2019] - Clear viewport defined by 2031-2034
	-- [2022] - Screen ratio (read only)
	-- [2023] - Hardware scale
	-- [2024] - Rotation (0 - 0*, 1 - 90*, 2 - 180*, 3 - 270*)
	-- [2025] - Brightness White
	-- [2026] - Brightness B
	-- [2027] - Brightness G
	-- [2028] - Brightness R
	-- [2029] - Vertical scale (1)
	-- [2030] - Horizontal scale (1)
	--
	-- Shifting control:
	-- [2031] - Low shift column
	-- [2032] - High shift column
	-- [2033] - Low shift row
	-- [2034] - High shift row
	--
	-- Character output control:
	-- [2035] - Charset, always 0
	-- [2036] - Brightness (additive)
	--
	-- Control registers:
	-- [2037] - Shift cells (number of cells, >0 right, <0 left)
	-- [2038] - Shift rows (number of rows, >0 shift up, <0 shift down)
	-- [2039] - Hardware Clear Row (Writing clears row)
	-- [2040] - Hardware Clear Column (Writing clears column)
	-- [2041] - Hardware Clear Screen
	-- [2042] - Hardware Background Color (000)
	--
	-- Cursor control:
	-- [2043] - Cursor Blink Rate (0.50)
	-- [2044] - Cursor Size (0.25)
	-- [2045] - Cursor Address
	-- [2046] - Cursor Enabled
	--
	-- [2047] - Clk

	self.Memory1[2022] = 3/4
	self.Memory1[2023] = 0
	self.Memory1[2024] = 0
	self.Memory1[2025] = 1
	self.Memory1[2026] = 1
	self.Memory1[2027] = 1
	self.Memory1[2028] = 1
	self.Memory1[2029] = 1
	self.Memory1[2030] = 1
	self.Memory1[2031] = 0
	self.Memory1[2032] = 29
	self.Memory1[2033] = 0
	self.Memory1[2034] = 17
	self.Memory1[2035] = 0
	self.Memory1[2036] = 0

	self.Memory1[2042] = 0
	self.Memory1[2043] = 0.5
	self.Memory1[2044] = 0.25
	self.Memory1[2045] = 0
	self.Memory1[2046] = 0
** **** **** **** **** ]#
