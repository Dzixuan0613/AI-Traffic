'''
Author: sh0829kk 381534335@qq.com
Date: 2023-02-08 15:25:37
LastEditors: sh0829kk 381534335@qq.com
LastEditTime: 2023-02-13 15:15:20
FilePath: /AI-Traffic/test.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#/usr/bin/python

def updateMetrics(conn,metrics,state,geometry):
    for lane in geometry["LaneID"]:
        metrics['WaitingTime'].append(conn.lane.getWaitingTime(lane))
        metrics['CO2'].append(conn.lane.getCO2Emission(lane))
            
    for vehicle in state["vehicleID"]:
        metrics['TimeLoss'].append(conn.vehicle.getTimeLoss(vehicle))
    return metrics