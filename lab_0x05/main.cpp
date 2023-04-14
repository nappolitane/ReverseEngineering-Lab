#include <Windows.h>
#include <iostream>
#include <TlHelp32.h>
#include <Psapi.h>
#include <conio.h>

int MyGetProcessId(const char* processName)
{
    PROCESSENTRY32 pe32;
    HANDLE hSnapshot = NULL;
    pe32.dwSize = sizeof(PROCESSENTRY32);
    hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);

    if (Process32First(hSnapshot, &pe32)) {
        do {
            std::wstring ws(pe32.szExeFile);
            std::string p_name(ws.begin(), ws.end());
            if (p_name.compare(processName) == 0)break;
        } while (Process32Next(hSnapshot, &pe32));
    }

    CloseHandle(hSnapshot);
    if (hSnapshot == INVALID_HANDLE_VALUE) {
        std::cout << "Process \"" << processName << "\" not found!" << std::endl;
        _getch();
        return -1;
    }

    return pe32.th32ProcessID;
}

char* MyReadMemory(HANDLE processHandle, int address, SIZE_T sz)
{
    char* rbuff = (char*)malloc(sz);
    SIZE_T NumberOfBytesToRead = sz;
    SIZE_T NumberOfBytesActuallyRead;
    BOOL err = ReadProcessMemory(processHandle, (LPCVOID)address, rbuff, NumberOfBytesToRead, &NumberOfBytesActuallyRead);
    if (err == 0) {
        free(rbuff);
        int erro = GetLastError();
        std::cout << erro << std::endl;
        std::cout << "An error occurred when reading!" << std::endl;
        _getch();
        return NULL;
    }
    return rbuff;
}

int MyWriteMemory(HANDLE processHandle, int address, char* memdump, int sz)
{
    char* wbuff = new char;
    wbuff[0] = (char)0xffffff8e;
    for (int i = 0; i < sz; i++) {
        if (memdump[i] == (char)0xffffff8f) {
            BOOL err = WriteProcessMemory(processHandle, (LPVOID)(address + i), (LPCVOID)wbuff, 1, NULL);
            if (err == 0) {
                delete[] wbuff;
                int erro = GetLastError();
                std::cout << erro << std::endl;
                std::cout << "An error occurred when writing!" << std::endl;
                _getch();
                return -1;
            }
        }
    }
    delete[] wbuff;
    return 0;
}

int main()
{
    int processId = MyGetProcessId("winmine.exe");
    if (processId == -1) return -1;

    HANDLE processHandle = OpenProcess(PROCESS_ALL_ACCESS, false, processId);

    int addrStart = 0x01005340;
    int addrEnd = 0x01005680;

    char* myMemoryDump = MyReadMemory(processHandle, addrStart, addrEnd - addrStart);
    if (myMemoryDump == NULL) return -1;

    int ret = MyWriteMemory(processHandle, addrStart, myMemoryDump, addrEnd - addrStart);
    free(myMemoryDump);
    myMemoryDump = NULL;
    if (ret == -1) return -1;

    CloseHandle(processHandle);

    std::cout << "Cracked!" << std::endl;
    std::cout << "Minimise the Minesweeper Window and then Maximise it again to refresh!" << std::endl;
    std::cout << "Press any key to continue ..." << std::endl;
    _getch();

    return 0;
}
