import sys
import wx

class KCad(wx.Frame):
    def __init__(self, parent, title):
        super(KCad, self).__init__(parent, title=title, size=(800, 600))

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.line_list = []

        self.start_position = None
        self.stop_position = None
        self.mouse_position = (0, 0)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMoved)

        self.Centre()
        self.Show()

    def OnClose(self, evt):
        self.Destroy()
        sys.exit(0)

    def OnMouseMoved(self, evt):
        self.mouse_position = evt.GetPosition()

    def OnPaint(self, evt):
        # TODO: Fix this to work on both Linux and Windows
        initial_dc = wx.ClientDC(self)
        dc = wx.BufferedDC(initial_dc)
        #dc = wx.BufferedPaintDC(self)
        dc.Clear()
        self.DrawLines(dc)

    def OnLeftDown(self, evt):
        if not self.start_position:
            self.start_position = evt.GetPosition()
            self.stop_position = None
        else:
            self.stop_position = evt.GetPosition()
            self.line_list.append((self.start_position[0],
                                  self.start_position[1],
                                  self.stop_position[0],
                                  self.stop_position[1]))
            self.start_position = None
            self.stop_position = None

    def OnRightDown(self, evt):
        pass

    def DrawLines(self, dc):
        dc.SetPen(wx.Pen('black', 1))
        dc.DrawLineList(self.line_list)

        # Current trace, if one is being drawn
        if self.start_position and not self.stop_position:
            # Check which part of the line to start drawing first
            # TODO: Need 45 degree angles too. See how KiCAD does it.
            vert_distance = abs(self.start_position[1] - self.mouse_position[1])
            horiz_distance = abs(self.start_position[0] - self.mouse_position[0])
            if vert_distance > horiz_distance:
                dc.DrawLine(self.start_position[0],
                            self.start_position[1],
                            self.start_position[0],
                            self.mouse_position[1])
                dc.DrawLine(self.start_position[0],
                            self.mouse_position[1],
                            self.mouse_position[0],
                            self.mouse_position[1])
            else:
                dc.DrawLine(self.start_position[0],
                            self.start_position[1],
                            self.mouse_position[0],
                            self.start_position[1])
                dc.DrawLine(self.mouse_position[0],
                            self.start_position[1],
                            self.mouse_position[0],
                            self.mouse_position[1])

        # Crosshairs
        # TODO: CrossHair function for full-width lines?
        dc.SetPen(wx.Pen('blue', 1))
        dc.DrawLine(self.mouse_position[0],
                    self.mouse_position[1] - 10,
                    self.mouse_position[0],
                    self.mouse_position[1] + 10)
        dc.DrawLine(self.mouse_position[0] - 10,
                    self.mouse_position[1],
                    self.mouse_position[0] + 10,
                    self.mouse_position[1])

        # Coordinates
        position_string = str(self.mouse_position[0]) + ', ' + str(self.mouse_position[1])
        dc.DrawText(position_string, 50, 50)

if __name__ == '__main__':
    app = wx.App()
    KCad(None, 'KCad')
    app.MainLoop()
