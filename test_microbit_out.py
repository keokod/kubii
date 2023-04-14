input.onButtonPressed(Button.A, function () {
    basic.showLeds(`
        # # # # #
        # . . . #
        # # # # #
        # . . . #
        # . . . #
        `)
})
input.onButtonPressed(Button.AB, function () {
    pins.digitalWritePin(DigitalPin.P9, 1)
    pins.digitalWritePin(DigitalPin.P10, 1)
    pins.digitalWritePin(DigitalPin.P11, 1)
    pins.digitalWritePin(DigitalPin.P12, 1)
    basic.pause(2000)
    pins.digitalWritePin(DigitalPin.P9, 0)
    pins.digitalWritePin(DigitalPin.P10, 0)
    pins.digitalWritePin(DigitalPin.P11, 0)
    pins.digitalWritePin(DigitalPin.P12, 0)
})
input.onButtonPressed(Button.B, function () {
    basic.showLeds(`
        # # # . .
        # . . # .
        # # # # .
        # . . # .
        # # # . .
        `)
})
basic.forever(function () {
    basic.showLeds(`
        . # . . .
        . # . . .
        . # . . .
        . # . . .
        . # . . .
        `)
    basic.pause(500)
    basic.showLeds(`
        . . # . .
        . . # . .
        . . # . .
        . . # . .
        . . # . .
        `)
    basic.pause(1000)
    basic.showLeds(`
        . . . # .
        . . . # .
        . . . # .
        . . . # .
        . . . # .
        `)
    basic.pause(500)
    basic.showLeds(`
        . . . . #
        . . . . #
        . . . . #
        . . . . #
        . . . . #
        `)
    basic.pause(500)
    basic.showLeds(`
        # . . . .
        # . . . .
        # . . . .
        # . . . .
        # . . . .
        `)
    basic.pause(500)
    pins.digitalWritePin(DigitalPin.P5, 1)
    basic.showLeds(`
        # # # # .
        # . . . .
        # # # # .
        . . . # .
        # # # # .
        `)
    basic.pause(500)
    pins.digitalWritePin(DigitalPin.P5, 0)
})
